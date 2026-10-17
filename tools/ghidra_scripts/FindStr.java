// FindStr.java - locate strings by regex, report referencing functions, optionally decompile them
//@category WeType
import ghidra.app.script.GhidraScript;
import ghidra.app.decompiler.*;
import ghidra.program.model.address.*;
import ghidra.program.model.listing.*;
import ghidra.program.model.mem.*;
import ghidra.program.model.symbol.*;
import ghidra.program.util.*;
import java.io.*;
import java.util.*;

public class FindStr extends GhidraScript {
    @Override
    public void run() throws Exception {
        String[] args = getScriptArgs();
        String outPath = args[0];
        String pattern = args[1];
        // support "@file": one regex per line, OR-joined. Works around cmd.exe mangling '|' in .bat args.
        if (pattern.startsWith("@")) {
            StringBuilder sb = new StringBuilder();
            BufferedReader pr = new BufferedReader(new FileReader(pattern.substring(1)));
            String line;
            while ((line = pr.readLine()) != null) {
                line = line.trim();
                if (line.isEmpty() || line.startsWith("#")) continue;
                if (sb.length() > 0) sb.append("|");
                sb.append(line);
            }
            pr.close();
            pattern = sb.toString();
        }
        boolean decompile = args.length > 2 && args[2].equalsIgnoreCase("decompile");
        int maxFuncs = args.length > 3 ? Integer.parseInt(args[3]) : 12;
        int maxDepth = args.length > 4 ? Integer.parseInt(args[4]) : 1;

        PrintWriter w = new PrintWriter(new BufferedWriter(new FileWriter(outPath), 1 << 20));
        Listing lst = currentProgram.getListing();
        Memory mem = currentProgram.getMemory();
        java.util.regex.Pattern rx = java.util.regex.Pattern.compile(pattern);

        w.println("PATTERN: " + pattern);
        w.println();

        // 1. find matching strings
        List<Data> hits = new ArrayList<>();
        DataIterator di = lst.getDefinedData(true);
        while (di.hasNext()) {
            Data d = di.next();
            if (d == null || d.getValue() == null) continue;
            String t = d.getValue().toString();
            if (rx.matcher(t).find()) hits.add(d);
        }
        w.println("=== MATCHING STRINGS: " + hits.size() + " ===");
        for (Data d : hits) w.println(d.getAddress() + "\t" + d.getDataType().getName() + "\t" + d.getValue());
        w.println();

        // 2. find code refs to each string
        Set<Function> funcs = new LinkedHashSet<>();
        w.println("=== STRING XREFS ===");
        ReferenceManager rm = currentProgram.getReferenceManager();
        for (Data d : hits) {
            Address a = d.getAddress();
            java.util.List<Reference> refs = new ArrayList<>();
            ReferenceIterator ri = rm.getReferencesTo(a);
            while (ri.hasNext()) refs.add(ri.next());
            w.println("--- " + d.getAddress() + " " + d.getValue() + "  refs=" + refs.size());
            for (Reference r : refs) {
                Address from = r.getFromAddress();
                Function f = getFunctionContaining(from);
                w.println("    from " + from + "  " + r.getReferenceType() + "  " + (f == null ? "(no func)" : f.getName() + "@" + f.getEntryPoint()));
                if (f != null) funcs.add(f);
            }
        }
        w.println();

        // 3. optionally walk callers (depth) and decompile
        Set<Function> expanded = new LinkedHashSet<>(funcs);
        for (int depth = 0; depth < maxDepth; depth++) {
            Set<Function> next = new LinkedHashSet<>();
            for (Function f : expanded) {
                for (Function c : f.getCallingFunctions(monitor)) next.add(c);
            }
            next.removeAll(expanded);
            if (next.isEmpty()) break;
            w.println("### CALLERS depth " + (depth + 1) + ": " + next.size());
            for (Function f : next) w.println("    " + f.getName() + "@" + f.getEntryPoint());
            expanded.addAll(next);
            if (expanded.size() > maxFuncs * 3) break;
        }
        w.println();

        if (decompile) {
            DecompInterface dec = new DecompInterface();
            dec.openProgram(currentProgram);
            DecompileOptions opt = new DecompileOptions();
            dec.setOptions(opt);
            int n = 0;
            w.println("=== DECOMPILED ===");
            for (Function f : expanded) {
                if (n >= maxFuncs) break;
                n++;
                w.println();
                w.println("////////////////////////////////////////////////////////////////");
                w.println("// FUNC " + f.getName() + " @" + f.getEntryPoint() + "  size=" + f.getBody().getNumAddresses());
                w.println("////////////////////////////////////////////////////////////////");
                try {
                    DecompileResults dr = dec.decompileFunction(f, 90, monitor);
                    if (dr != null && dr.decompileCompleted()) w.println(dr.getDecompiledFunction().getC());
                    else w.println("// decompile failed: " + (dr == null ? "null" : dr.getErrorMessage()));
                } catch (Exception e) { w.println("// exception: " + e); }
            }
            w.println();
            w.println("// decompiled " + n + " functions");
            dec.dispose();
        }
        w.close();
        println("FindStr done -> " + outPath);
    }
}
