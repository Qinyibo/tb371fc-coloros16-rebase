import java.nio.file.*;
import java.io.*;
import java.util.regex.*;
import com.android.tools.smali.dexlib2.*;
import com.android.tools.smali.dexlib2.iface.*;
import com.android.tools.smali.baksmali.*;
import com.android.tools.smali.baksmali.Adaptors.ClassDefinition;
import com.android.tools.smali.baksmali.formatter.BaksmaliWriter;
public final class ExportRebaseContext {
 public static void main(String[] args)throws Exception{
 var out=Paths.get(args[1]);Files.createDirectories(out);
 var regex=Pattern.compile(args.length > 2 ? args[2] : "(OplusBatteryServiceFeature|CachedAppOptimizerExtImpl|HansManager|HansNativeService|/charger/ICharger)");
 var container=DexFileFactory.loadDexContainer(new File(args[0]),Opcodes.forApi(36));var opt=new BaksmaliOptions();opt.apiLevel=36;int count=0;
 for(String entry:container.getDexEntryNames())for(ClassDef def:container.getEntry(entry).getDexFile().getClasses()){
 if(!regex.matcher(def.getType()).find())continue;
 var path=out.resolve(def.getType().substring(1,def.getType().length()-1)+".smali");Files.createDirectories(path.getParent());
 try(var w=new BaksmaliWriter(Files.newBufferedWriter(path))){new ClassDefinition(opt,def).writeTo(w);}count++;
 }System.out.println("COMPLETE_REBASE_CONTEXT_CLASSES="+count);
 }
}
