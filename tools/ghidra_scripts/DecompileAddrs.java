// DecompileAddrs.java - decompile a list of function entry addresses from a text file
//@category WeType
import ghidra.app.script.GhidraScript;
import ghidra.app.decompiler.*;
import ghidra.program.model.address.Address;
import ghidra.program.model.listing.*;
import java.io.*;
import java.util.*;

public class DecompileAddrs extends GhidraScript {
    @Override
    public void run() throws Exception {
        String[] args = getScriptArgs();
        String outPath = args[0];
        String addrFile = args[1];
        int maxF = args.length > 2 ? Integer.parseInt(args[2]) : 40;
        PrintWriter w = new PrintWriter(new BufferedWriter(new FileWriter(outPath), 1 << 20));
        DecompInterface dec = new DecompInterface();
        dec.openProgram(currentProgram);
        DecompileOptions opt = new DecompileOptions();
        dec.setOptions(opt);
        BufferedReader r = new BufferedReader(new FileReader(addrFile));
        String line; int n = 0;
        List<String> labels = new ArrayList<>();
        while ((line = r.readLine()) != null) {
            line = line.trim();
            if (line.isEmpty() || line.startsWith("#")) continue;
            String label = "";
            int sp = line.indexOf(' ');
            if (sp > 0) { label = line.substring(sp + 1).trim(); line = line.substring(0, sp).trim(); }
            if (n >= maxF) break;
            n++;
            Address a;
            try { a = toAddr(line); } catch (Exception e) { w.println("// bad addr " + line); continue; }
            Function f = getFunctionAt(a);
            w.println();
            w.println("////////////////////////////////////////////////////////////////");
            w.println("// " + label + "  FUNC " + (f == null ? "(none)" : f.getName()) + " @" + a);
            w.println("////////////////////////////////////////////////////////////////");
            if (f == null) {
                // try to create one
                try {
                    f = createFunction(a, null);
                } catch (Exception e) {}
            }
            if (f == null) { w.println("// no function at " + a); continue; }
            try {
                DecompileResults dr = dec.decompileFunction(f, 90, monitor);
                if (dr != null && dr.decompileCompleted()) w.println(dr.getDecompiledFunction().getC());
                else w.println("// decompile failed: " + (dr == null ? "null" : dr.getErrorMessage()));
            } catch (Exception e) { w.println("// exception: " + e); }
        }
        r.close();
        w.println();
        w.println("// decompiled " + n);
        w.close();
        dec.dispose();
        println("DecompileAddrs done -> " + outPath);
    }
}