import ghidra.app.script.GhidraScript;
import ghidra.program.model.listing.*;
import ghidra.program.model.symbol.*;
import ghidra.program.model.address.*;
import ghidra.program.model.mem.*;
import java.io.*;
import java.util.*;

public class IndexDump extends GhidraScript {
    public void run() throws Exception {
        String[] a = getScriptArgs();
        String out = a[0];
        boolean full = a.length > 1 && a[1].equals("full");
        PrintWriter w = new PrintWriter(new BufferedWriter(new FileWriter(out)));
        Program p = currentProgram;
        w.println("PROGRAM " + p.getName());
        w.println("EXECUTABLE_PATH " + p.getExecutablePath());
        w.println("LANGUAGE " + p.getLanguageID());
        w.println("COMPILER " + p.getCompiler());
        w.println("IMAGEBASE " + p.getImageBase());
        w.println("MD5 " + p.getExecutableMD5());
        w.println("SHA256 " + p.getExecutableSHA256());
        w.println("FORMAT " + p.getExecutableFormat());
        w.println();
        w.println("=== MEMORY BLOCKS ===");
        for (MemoryBlock b : p.getMemory().getBlocks()) {
            w.printf("%s %s-%s size=0x%x r=%b w=%b x=%b init=%b%n", b.getName(), b.getStart(), b.getEnd(), b.getSize(), b.isRead(), b.isWrite(), b.isExecute(), b.isInitialized());
        }
        w.println();
        w.println("=== FUNCTIONS ===");
        FunctionManager fm = p.getFunctionManager();
        int n = 0;
        for (Function f : fm.getFunctions(true)) {
            w.printf("%s\t%s\t%s\t%d%s%n", f.getEntryPoint(), f.getName(), f.getPrototypeString(false, false), f.getBody().getNumAddresses(), f.isThunk() ? "\tthunk" : "");
            n++;
        }
        w.println("TOTAL_FUNCTIONS " + n);
        w.println();
        w.println("=== IMPORTS/EXTERNAL SYMBOLS ===");
        SymbolTable st = p.getSymbolTable();
        SymbolIterator it = st.getExternalSymbols();
        int ic = 0;
        while (it.hasNext()) { w.println(it.next().getName()); ic++; }
        w.println("TOTAL_EXTERNALS " + ic);
        w.println();
        w.println("=== STRINGS (defined) ===");
        DataIterator di = p.getListing().getDefinedData(true);
        int sc = 0;
        while (di.hasNext()) {
            Data d = di.next();
            if (d == null) continue;
            Object v = d.getValue();
            if (v instanceof String) {
                w.printf("%s\t%s\t%s%n", d.getAddress(), d.getDataType().getName(), ((String) v).replace("\n", "\\n").replace("\t", "\\t"));
                sc++;
            }
        }
        w.println("TOTAL_STRINGS " + sc);
        if (full) {
            w.println();
            w.println("=== ALL SYMBOLS ===");
            int sn = 0;
            for (Symbol s : st.getAllSymbols(true)) {
                w.printf("%s\t%s\t%s%n", s.getAddress(), s.getName(), s.getSymbolType());
                sn++;
            }
            w.println("TOTAL_SYMBOLS " + sn);
        }
        w.close();
        println("IndexDump written: " + out);
    }
}
