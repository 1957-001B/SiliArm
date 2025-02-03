.global _main        ; Make start symbol visible to linker
_main:              ; Entry point
    ORR X0, XZR, 1  ; This one is fine
    ADD X0, X0, 5
    ORR X1, XZR, 2  ; Changed from 42 to 2 as it's a valid logical immediate
    ADD X1, X1, X0
    B 0x4000
    ORR X3, XZR, 4  ; Changed from 100 to 4 as it's a valid logical immediate
    ADD X2, X2, 1
    B 0x1000
loop:
    ADD X2, X1, 1
    b .loop
    MOV X16, #1     ; Exit syscall number for macOS
    SVC #0x80       ; Make syscall