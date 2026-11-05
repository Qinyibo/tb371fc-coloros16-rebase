import java.nio.file.*;
import java.io.*;
import java.util.*;
import java.util.regex.*;
import com.android.tools.smali.dexlib2.*;
import com.android.tools.smali.dexlib2.iface.*;
import com.android.tools.smali.baksmali.*;
import com.android.tools.smali.baksmali.Adaptors.ClassDefinition;
import com.android.tools.smali.baksmali.formatter.BaksmaliWriter;
public class CompareDex {
 static Map<String,String> read(String path)throws Exception {
  var result=new TreeMap<String,String>();var opt=new BaksmaliOptions();opt.apiLevel=36;
  var dex=DexFileFactory.loadDexFile(new File(path),Opcodes.forApi(36));
  var pattern=Pattern.compile("(?ms)^\\.method ([^\\n]+)\\n.*?^\\.end method");
  for(var c:dex.getClasses()) {
   var s=new StringWriter();try(var w=new BaksmaliWriter(s)){new ClassDefinition(opt,c).writeTo(w);}
   var m=pattern.matcher(s.toString());while(m.find())result.put(c.getType()+"->"+m.group(1).trim(),m.group());
   result.put(c.getType()+"#metadata",pattern.matcher(s.toString()).replaceAll("").replaceAll("(?m)^(\\.field [^\\r\\n]+:Z) = false\\r?$", "$1"));
  }
  return result;
 }
 public static void main(String[] a)throws Exception {
  var before=read(a[0]);var after=read(a[1]);if(!before.keySet().equals(after.keySet()))throw new Error("members changed");
  var changed=new ArrayList<String>();for(var k:before.keySet())if(!before.get(k).equals(after.get(k)))changed.add(k);
  var expected=a.length>3?Set.of(Arrays.copyOfRange(a,3,a.length)):Set.of("Lcom/android/server/OplusBatteryServiceFeature;->public getChgConfig(ILjava/lang/String;I)Ljava/lang/String;","Lcom/android/server/am/CachedAppOptimizerExtImpl;->public checkFreezeProc(Lcom/android/server/am/ProcessRecord;)Z");
  if(!new HashSet<>(changed).equals(expected)){ Files.createDirectories(Path.of(a[2])); for(var k:changed)if(k.endsWith("#metadata")){var n=k.replaceAll("[^a-zA-Z0-9]","_");Files.writeString(Path.of(a[2],n+".before"),before.get(k));Files.writeString(Path.of(a[2],n+".after"),after.get(k));} throw new Error(changed.toString());}
  System.out.println("CANONICAL_DEX_COMPARE_PASS members="+before.size()+" changed="+changed);
 }
}
