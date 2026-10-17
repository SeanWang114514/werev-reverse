// VtableDump.java - dump RTTI-derived vtables and their function pointers
//@category WeType
import ghidra.app.script.GhidraScript;
import ghidra.program.model.address.Address;
import ghidra.program.model.listing.*;
import ghidra.program.model.mem.*;
import ghidra.program.model.symbol.*;
import java.io.*;
import java.util.*;

public class VtableDump extends GhidraScript {
    @Override
    public void run() throws Exception {
        String[] args = getScriptArgs();
        String outPath = args[0];
        int maxPerTable = args.length > 1 ? Integer.parseInt(args[1]) : 64;
        PrintWriter w = new PrintWriter(new BufferedWriter(new FileWriter(outPath), 1 << 20));
        Listing lst = currentProgram.getListing();
        Memory mem = currentProgram.getMemory();
        SymbolTable st = currentProgram.getSymbolTable();

        // Collect all vftable labels
        List<Symbol> vts = new ArrayList<>();
        for (Symbol s : st.getAllSymbols(true)) {
            String n = s.getName();
            if (n.contains("vftable") || n.contains("vtable")) vts.add(s);
        }
        w.println("# vftable symbols: " + vts.size());
        w.println();

        // Also collect RTTI type descriptor strings for class inventory
        DataIterator di = lst.getDefinedData(true);
        int rttiCount = 0;
        w.println("=== RTTI TYPE DESCRIPTORS ===");
        while (di.hasNext()) {
            Data d = di.next();
            if (d == null || d.getValue() == null) continue;
            String v = d.getValue().toString();
            if (v.startsWith(".?AV") || v.startsWith(".?AU")) {
                w.println(d.getAddress() + "\t" + v);
                rttiCount++;
            }
        }
        w.println("# rtti descriptors: " + rttiCount);
        w.println();

        w.println("=== VFTABLES ===");
        for (Symbol s : vts) {
            Address a = s.getAddress();
            String nm = s.getName(true);
            w.println("### " + a + "\t" + nm);
            Address p = a;
            for (int i = 0; i < maxPerTable; i++) {
                try {
                    long v = mem.getLong(p);
                    Address tgt = toAddr(v);
                    String fn = "?";
                    Function f = getFunctionAt(tgt);
                    if (f != null) fn = f.getName();
                    else {
                        Data dd = lst.getDataAt(tgt);
                        if (dd != null) fn = "[" + dd.getValue() + "]";
                        else fn = "(no function)";
                    }
                    w.println("    [" + i + "] " + p + " -> " + tgt + "  " + fn);
                    p = p.add(8);
                    // stop when we hit something that is not a code pointer in .text
                    if (getFunctionAt(tgt) == null && lst.getDataAt(tgt) == null) break;
                } catch (Exception e) {
                    break;
                }
            }
        }
        w.close();
        println("VtableDump done -> " + outPath);
    }
}
