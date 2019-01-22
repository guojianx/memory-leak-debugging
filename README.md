# python_tools

Debug Memory Leak With GDB:
First of all, that's necessary to find out the right breakpoint (such as leaveq) in a functioni by 'disassemble' command, at that point we can access the return value of the function with the register rax.
(gdb) info breakpoints 
Num     Type           Disp Enb Address            What
1       hw breakpoint  keep n   0x00000000015ad7eb in av_malloc at libavutil/mem.c:133
    breakpoint already hit 15 times
        shell date +"%F %T"
        printf "0x%016llx, av_malloc, %ld\n", $rax, size
        where
        continue
2       hw breakpoint  keep y   0x00000000015ad9f9 in av_free at libavutil/mem.c:211
    stop only if ptr != 0
    breakpoint already hit 13 times
        shell date +"%F %T"
        printf "0x%016llx, av_free\n", ptr
        where
        continue
3       hw breakpoint  keep y   0x00000000015ad836 in av_realloc at libavutil/mem.c:146
    breakpoint already hit 3 times
        shell date +"%F %T"
        printf "0x%016llx, av_realloc, 0x%016llx, %ld\n", $rax, ptr, size
        where
        continue

