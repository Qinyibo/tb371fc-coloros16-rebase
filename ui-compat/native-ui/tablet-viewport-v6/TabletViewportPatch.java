import java.nio.file.*;
import java.util.*;
import com.android.tools.smali.dexlib2.*;
import com.android.tools.smali.dexlib2.builder.*;
import com.android.tools.smali.dexlib2.builder.instruction.*;
import com.android.tools.smali.dexlib2.dexbacked.*;
import com.android.tools.smali.dexlib2.iface.*;
import com.android.tools.smali.dexlib2.iface.instruction.*;
import com.android.tools.smali.dexlib2.iface.reference.*;
import com.android.tools.smali.dexlib2.immutable.*;
import com.android.tools.smali.dexlib2.immutable.reference.*;
import com.android.tools.smali.dexlib2.writer.pool.DexPool;

class TabletViewportPatch {
 static final String CELL="Lcom/android/launcher/layoutparam/CellLayoutParam;";
 static final String WORK="Lcom/android/launcher/layoutparam/WorkspaceParam;";
 static final String HELPER="Lorg/tb371fc/layout/TabletViewport;";
 public static void main(String[] args) throws Exception {
  var dex=new DexBackedDexFile(Opcodes.forApi(36),Files.readAllBytes(Path.of(args[0])));
  var classes=new ArrayList<ClassDef>();
  int changes=0;
  for(var type:dex.getClasses()) {
   var methods=new ArrayList<Method>();
   boolean changed=false;
   for(var method:type.getMethods()) {
    com.android.tools.smali.dexlib2.iface.MethodImplementation implementation=method.getImplementation();
    if(type.getType().equals(CELL)&&method.getName().equals("getCellHeight")&&method.getParameterTypes().equals(List.of("I","I","Z","Z"))) {
     var body=new MutableMethodImplementation(implementation);
     if(body.getRegisterCount()!=12)throw new IllegalStateException("cell registers");
     int count=0;
     for(int i=1;i<body.getInstructions().size();i++) {
      var ins=body.getInstructions().get(i);
      if(ins instanceof ReferenceInstruction ref&&ref.getReference() instanceof MethodReference call&&call.getDefiningClass().equals("Ljava/lang/Math;")&&call.getName().equals("min")) {
       var prev=body.getInstructions().get(i-1);
       if(prev.getOpcode()!=Opcode.IGET||!(prev instanceof ReferenceInstruction r)||!(r.getReference() instanceof FieldReference f)||!f.getName().equals("phoneViewportMaxCellHeightPx"))throw new IllegalStateException("cap layout");
       body.addInstruction(i-1,new BuilderInstruction35c(Opcode.INVOKE_VIRTUAL,1,7,0,0,0,0,
        new ImmutableMethodReference(CELL,"getWorkspace",List.of(),WORK)));
       body.addInstruction(i,new BuilderInstruction11x(Opcode.MOVE_RESULT_OBJECT,2));
       body.replaceInstruction(i+2,new BuilderInstruction35c(Opcode.INVOKE_STATIC,5,0,7,2,8,9,
        new ImmutableMethodReference(HELPER,"cellHeight",List.of("I","I",WORK,"I","I"),"I")));
       count++;i+=3;
      }
     }
     if(count!=1)throw new IllegalStateException("cell cap call count");
     implementation=body;changed=true;changes++;
    }
    methods.add(new ImmutableMethod(type.getType(),method.getName(),method.getParameters(),method.getReturnType(),
      method.getAccessFlags(),method.getAnnotations(),method.getHiddenApiRestrictions(),implementation));
   }
   classes.add(changed?new ImmutableClassDef(type.getType(),type.getAccessFlags(),type.getSuperclass(),type.getInterfaces(),type.getSourceFile(),type.getAnnotations(),type.getFields(),methods):type);
  }
  if(changes>0)DexPool.writeTo(args[1],new ImmutableDexFile(dex.getOpcodes(),classes));
  System.out.println("CHANGES "+changes);
 }
}
