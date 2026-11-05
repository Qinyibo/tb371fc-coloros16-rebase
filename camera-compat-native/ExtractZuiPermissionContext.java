import java.io.File;
import java.nio.file.Files;
import java.nio.file.Path;
import java.util.Set;
import com.android.tools.smali.dexlib2.DexFileFactory;
import com.android.tools.smali.dexlib2.Opcodes;
import com.android.tools.smali.dexlib2.iface.instruction.ReferenceInstruction;
import com.android.tools.smali.dexlib2.iface.reference.StringReference;
import com.android.tools.smali.baksmali.BaksmaliOptions;
import com.android.tools.smali.baksmali.Adaptors.ClassDefinition;
import com.android.tools.smali.baksmali.formatter.BaksmaliWriter;

class ExtractZuiPermissionContext {
    public static void main(String[] args) throws Exception {
        var permissions = Set.of("android.permission.READ_MEDIA_IMAGES", "android.permission.WRITE_EXTERNAL_STORAGE");
        var dex = DexFileFactory.loadDexContainer(new File(args[0]), Opcodes.forApi(33));
        var options = new BaksmaliOptions();
        options.apiLevel = 33;
        for (var entry : dex.getDexEntryNames()) {
            for (var type : dex.getEntry(entry).getDexFile().getClasses()) {
                String name = type.getType();
                if (name.startsWith("Landroid") || name.startsWith("Lkotlin")) {
                    continue;
                }
                boolean found = name.equals("Lcom/zui/camera/CameraLauncher;");
                for (var method : type.getMethods()) {
                    if (method.getImplementation() == null) {
                        continue;
                    }
                    for (var instruction : method.getImplementation().getInstructions()) {
                        if (instruction instanceof ReferenceInstruction ref && ref.getReference() instanceof StringReference text
                            && permissions.contains(text.getString())) {
                            System.out.println(name + " " + method.getName() + " " + text.getString());
                            found = true;
                        }
                    }
                }
                if (found) {
                    var file = Path.of(args[1], name.substring(1, name.length() - 1) + ".smali");
                    Files.createDirectories(file.getParent());
                    try (var writer = new BaksmaliWriter(Files.newBufferedWriter(file))) {
                        new ClassDefinition(options, type).writeTo(writer);
                    }
                }
            }
        }
    }
}
