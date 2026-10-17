import ghidra.app.script.GhidraScript;
import ghidra.app.decompiler.*;
import ghidra.program.model.listing.*;
import java.io.*;
import java.util.*;
import java.util.regex.*;

public class DecompileFuncs extends GhidraScript {
    public void run() throws Exception {
        String[] a = getScriptArgs();
        String out = a[0];
        String filter = a.length > 1 ? a[1] : ".*";
        int max = a.length > 2 ? Integer.parseInt(a[2]) : 100000;
        int timeout = a.length > 3 ? Integer.parseInt(a[3]) : 120;
        Pattern rx = Pattern.compile(filter);
        DecompInterface di = new DecompInterface();
        di.toggleCCode(true);
        di.toggleSyntaxTree(true);
        di.openProgram(currentProgram);
        PrintWriter w = new PrintWriter(new BufferedWriter(new FileWriter(out)));
        FunctionManager fm = currentProgram.getFunctionManager();
        int n = 0, ok = 0;
        for (Function f : fm.getFunctions(true)) {
            if (!rx.matcher(f.getName()).find()) continue;
            if (n >= max) break;
            n++;
            w.println("/* ============================================================ */");
            w.printf("/* FUNC %s  %s%n", f.getEntryPoint(), f.getPrototypeString(false, false));
            w.println("/* ============================================================ */");
            try {
                DecompileResults r = di.decompileFunction(f, timeout, monitor);
                if (r != null && r.decompileCompleted()) { w.println(r.getDecompiledFunction().getC()); ok++; }
                else { w.println("/* decompile failed: " + (r == null ? "null" : r.getErrorMessage()) + " */"); }
            } catch (Exception e) { w.println("/* exception: " + e + " */"); }
            w.println();
        }
        w.printf("/* SUMMARY matched=%d decompiled=%d */%n", n, ok);
        w.close();
        di.dispose();
        println("DecompileFuncs written: " + out + " n=" + n + " ok=" + ok);
    }
}
