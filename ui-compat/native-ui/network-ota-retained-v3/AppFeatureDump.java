import java.io.*;
import java.util.*;
import java.util.zip.*;
import com.android.tools.smali.dexlib2.*;
import com.android.tools.smali.dexlib2.dexbacked.*;
import com.android.tools.smali.baksmali.*;
public class AppFeatureDump {
 public static void main(String[] args) throws Exception {
  List<String> selected=List.of("Lcom/oplus/customize/appfeature/k;","Lcom/oplus/customize/appfeature/d;","Lcom/oplus/customize/appfeature/c;","Lcom/oplus/customize/appfeature/f;","Lcom/oplus/customize/appfeature/h;");
  try(ZipFile z=new ZipFile(args[0])) {
   for(ZipEntry e:Collections.list(z.entries())) {
    if(!e.getName().matches("classes[0-9]*\\.dex"))continue;
    DexBackedDexFile dex=DexBackedDexFile.fromInputStream(Opcodes.getDefault(),new BufferedInputStream(z.getInputStream(e)));
    BaksmaliOptions opt=new BaksmaliOptions(); opt.debugInfo=false;
    if(!Baksmali.disassembleDexFile(dex,new File(args[1]),1,opt,selected))throw new IOException("Disassembly failed");
   }
  }
 }
}
