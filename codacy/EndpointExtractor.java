import com.github.javaparser.StaticJavaParser;
import com.github.javaparser.ast.CompilationUnit;
import com.github.javaparser.ast.body.MethodDeclaration;
import com.github.javaparser.ast.visitor.VoidVisitorAdapter;
import java.io.File;
import java.io.FileWriter;
import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.Paths;
import java.util.Arrays;
import java.util.List;
import java.util.Optional;
import org.apache.commons.lang3.tuple.Pair;

public class EndpointExtractor {
    public static void main(String[] args) throws IOException {
        if (args.length < 2) {
            System.out.println("Usage: java -jar EndpointExtractor.jar <project_path> <custom_annotation1> <custom_annotation2> ...");
            System.exit(1);
        }

        String projectPath = args[0];
        List<String> customAnnotations = Arrays.asList(Arrays.copyOfRange(args, 1, args.length));

        Files.walk(Paths.get(projectPath))
            .filter(Files::isRegularFile)
            .filter(path -> path.toString().endsWith(".java"))
            .forEach(path -> processJavaFile(path.toFile(), customAnnotations));
    }

    private static void processJavaFile(File file, List<String> customAnnotations) {
        try {
            CompilationUnit cu = StaticJavaParser.parse(file);
            new MethodVisitor(customAnnotations).visit(cu, null);
        } catch (IOException e) {
            e.printStackTrace();
        }
    }

    private static class MethodVisitor extends VoidVisitorAdapter<Void> {
        private String currentClassPath = "";
        private List<String> customAnnotations;
    
        public MethodVisitor(List<String> customAnnotations) {
            this.customAnnotations = customAnnotations;
        }

        @Override
        public void visit(ClassOrInterfaceDeclaration cid, Void arg) {
            super.visit(cid, arg);
            Optional<AnnotationExpr> classAnnotation = cid.getAnnotationByClass(RequestMapping.class);
            if (classAnnotation.isPresent()) {
                Pair<String, String> classEndpointInfo = extractEndpointInfo(classAnnotation.get());
                currentClassPath = classEndpointInfo.getFirst();
            } else {
                currentClassPath = "";
            }
        }

        @Override
        public void visit(MethodDeclaration md, Void arg) {
            super.visit(md, arg);
            md.getAnnotations().stream()
                .filter(annotation -> annotation.getNameAsString().endsWith("Mapping") || customAnnotations.contains(annotation.getNameAsString()))
                .forEach(annotation -> {
                    Pair<String, String> methodEndpointInfo = extractEndpointInfo(annotation);
                    String fullPath = currentClassPath + methodEndpointInfo.getFirst();
                    writeEndpointToFile(md, annotation, fullPath, methodEndpointInfo.getSecond());
                });
        }

        private void writeEndpointToFile(MethodDeclaration md, AnnotationExpr annotation, String fullPath, String httpMethod) {
            String endpointPath = fullPath.replace("/", "-");
            try {
                Path outputDir = Paths.get("/spring_output");
                if (!Files.exists(outputDir)) {
                    Files.createDirectories(outputDir);
                }
                try (FileWriter writer = new FileWriter(outputDir.resolve(endpointPath + "-" + httpMethod + ".java").toFile())) {
                    writer.write(md.toString());
                }
            } catch (IOException e) {
                e.printStackTrace();
            }
        }
        
        private Pair<String, String> extractEndpointInfo(AnnotationExpr annotation) {
            String path = "";
            String method = "";
            if (annotation.isSingleMemberAnnotationExpr()) {
                path = annotation.asSingleMemberAnnotationExpr().getMemberValue().toString().replaceAll("\"", "");
            } else if (annotation.isNormalAnnotationExpr()) {
                for (MemberValuePair pair : annotation.asNormalAnnotationExpr().getPairs()) {
                    if (pair.getNameAsString().equals("value") || pair.getNameAsString().equals("path")) {
                        path = pair.getValue().toString().replaceAll("\"", "");
                        if (pair.getValue().isFieldAccessExpr()) {
                            path = pair.getValue().asFieldAccessExpr().getNameAsString();
                        }
                    } else if (pair.getNameAsString().equals("method")) {
                        method = pair.getValue().toString().replaceAll("RequestMethod.", "");
                        if (pair.getValue().isFieldAccessExpr()) {
                            method = pair.getValue().asFieldAccessExpr().getNameAsString();
                        }
                    }
                }
            }
            return new Pair<>(path, method);
        }
    }
}