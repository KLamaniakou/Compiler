L1: 
sw ra,(sp)
L2: 
lw t1,-16(sp)
li t2,1
add ,t1, t1,t2 
sw t1,-20(sp)
L3: 
lw t1,-20(sp)
sw t1,-16(sp)
L4: 
lw t1,-16(gp)
lw t2,-20(gp)
bgt ,t1, t2, L6
L5: 
j L10
L6: 
lw t1,-16(gp)
lw t2,-24(gp)
bgt ,t1, t2, L8
L7: 
j L10
L8: 
lw t1,-16(gp)
sw t1,-12(sp)
L9: 
j L16
L10: 
lw t1,-20(gp)
lw t2,-16(gp)
bgt ,t1, t2, L12
L11: 
j L_
L12: 
lw t1,-20(gp)
lw t2,-24(gp)
bgt ,t1, t2, L14
L13: 
j L_
L14: 
lw t1,-20(gp)
sw t1,-12(sp)
L15: 
lw t1,-24(gp)
sw t1,-12(sp)
L16: 
lw t1,-12(sp)
lw t0, -8(sp)
sw t1, 0(t0)
lw ra, 0(sp)
jr ra
L17: 
lw ra,(sp)
jr ra
L18: 
sw ra,(sp)
L19: 
lw t1,-12(sp)
li t2,1
add ,t1, t1,t2 
sw t1,-16(sp)
L20: 
lw t1,-16(sp)
sw t1,-12(sp)
L21: 
lw t1,-16(gp)
li t2,0
blt ,t1, t2, L23
L22: 
j L25
L23: 
li t1,1
lw t0, -8(sp)
sw t1, 0(t0)
lw ra, 0(sp)
jr ra
L24: 
j L40
L25: 
lw t1,-16(gp)
li t2,0
beq ,t1, t2, L29
L26: 
j L27
L27: 
lw t1,-16(gp)
li t2,1
beq ,t1, t2, L29
L28: 
j L_
L29: 
li t1,1
lw t0, -8(sp)
sw t1, 0(t0)
lw ra, 0(sp)
jr ra
L30: 
lw t1,-16(gp)
li t2,1
sub ,t1, t1,t2 
sw t1,-20(sp)
L31: 
addi fp,sp,40
lw t0,-20(sp)
sw t0, -12(fp)
L32: 
addi t0,sp,-24
sw t0, -8(fp)
L33: 
lw t0,-4(sp)
sw t0,-4(fp)
addi sp,sp,40
jal L18
addi sp,sp,-40
L34: 
lw t1,-16(gp)
li t2,2
sub ,t1, t1,t2 
sw t1,-28(sp)
L35: 
addi fp,sp,40
lw t0,-28(sp)
sw t0, -12(fp)
L36: 
addi t0,sp,-32
sw t0, -8(fp)
L37: 
lw t0,-4(sp)
sw t0,-4(fp)
addi sp,sp,40
jal L18
addi sp,sp,-40
L38: 
lw t1,-24(sp)
lw t2,-32(sp)
add ,t1, t1,t2 
sw t1,-36(sp)
L39: 
lw t1,-36(sp)
lw t0, -8(sp)
sw t1, 0(t0)
lw ra, 0(sp)
jr ra
L40: 
lw ra,(sp)
jr ra
L41: 
sw ra,(sp)
L42: 
sw ra,(sp)
L43: 
lw t1,-12(sp)
li t2,1
add ,t1, t1,t2 
sw t1,-16(sp)
L44: 
lw t1,-16(sp)
sw t1,-12(sp)
L45: 
lw t0,-4(sp)
addi t0,t0,-20
lw t1,(t0)
lw t0,-4(sp)
addi t0,t0,-16
lw t2,(t0)
div ,t1, t1,t2 
sw t1,-20(sp)
L46: 
lw t1,-20(sp)
lw t0,-4(sp)
addi t0,t0,-16
lw t2,(t0)
mul ,t1, t1,t2 
sw t1,-24(sp)
L47: 
lw t0,-4(sp)
addi t0,t0,-20
lw t1,(t0)
lw t2,-24(sp)
beq ,t1, t2, L49
L48: 
j L51
L49: 
li t1,1
lw t0, -8(sp)
sw t1, 0(t0)
lw ra, 0(sp)
jr ra
L50: 
j L52
L51: 
li t1,0
lw t0, -8(sp)
sw t1, 0(t0)
lw ra, 0(sp)
jr ra
L52: 
lw ra,(sp)
jr ra
L53: 
lw t1,-24(sp)
li t2,1
add ,t1, t1,t2 
sw t1,-28(sp)
L54: 
lw t1,-28(sp)
sw t1,-24(sp)
L55: 
li t1,2
sw t1,-12(sp)
L56: 
lw t1,-12(sp)
lw t2,-16(sp)
blt ,t1, t2, L58
L57: 
j L69
L58: 
addi fp,sp,28
lw t0,-12(sp)
sw t0, -12(fp)
L59: 
lw t0,-16(sp)
sw t0, -16(fp)
L60: 
addi t0,sp,-32
sw t0, -8(fp)
L61: 
sw sp,-4(fp)
addi sp,sp,28
jal L42
addi sp,sp,-28
L62: 
lw t1,-32(sp)
li t2,1
beq ,t1, t2, L64
L63: 
j L66
L64: 
li t1,0
lw t0, -8(sp)
sw t1, 0(t0)
lw ra, 0(sp)
jr ra
L65: 
j L_
L66: 
lw t1,-12(sp)
li t2,1
add ,t1, t1,t2 
sw t1,-36(sp)
L67: 
lw t1,-36(sp)
sw t1,-12(sp)
L68: 
j L56
L69: 
li t1,1
lw t0, -8(sp)
sw t1, 0(t0)
lw ra, 0(sp)
jr ra
L70: 
lw ra,(sp)
jr ra
L71: 
sw ra,(sp)
L72: 
sw ra,(sp)
L73: 
lw t1,-12(sp)
li t2,1
add ,t1, t1,t2 
sw t1,-16(sp)
L74: 
lw t1,-16(sp)
sw t1,-12(sp)
L75: 
lw t0,-4(sp)
addi t0,t0,-16
lw t1,(t0)
lw t0,-4(sp)
addi t0,t0,-16
lw t2,(t0)
mul ,t1, t1,t2 
sw t1,-20(sp)
L76: 
lw t1,-20(sp)
lw t0, -8(sp)
sw t1, 0(t0)
lw ra, 0(sp)
jr ra
L77: 
lw ra,(sp)
jr ra
L78: 
lw t1,-20(sp)
li t2,1
add ,t1, t1,t2 
sw t1,-24(sp)
L79: 
lw t1,-24(sp)
sw t1,-20(sp)
L80: 
addi fp,sp,24
lw t0,-16(sp)
sw t0, -12(fp)
L81: 
addi t0,sp,-28
sw t0, -8(fp)
L82: 
sw sp,-4(fp)
addi sp,sp,24
jal L72
addi sp,sp,-24
L83: 
addi fp,sp,24
lw t0,-16(sp)
sw t0, -12(fp)
L84: 
addi t0,sp,-32
sw t0, -8(fp)
L85: 
sw sp,-4(fp)
addi sp,sp,24
jal L72
addi sp,sp,-24
L86: 
lw t1,-28(sp)
lw t2,-32(sp)
mul ,t1, t1,t2 
sw t1,-36(sp)
L87: 
lw t1,-36(sp)
sw t1,-12(sp)
L88: 
lw t1,-12(sp)
lw t0, -8(sp)
sw t1, 0(t0)
lw ra, 0(sp)
jr ra
L89: 
lw ra,(sp)
jr ra
L90: 
sw ra,(sp)
L91: 
lw t1,-12(sp)
li t2,1
add ,t1, t1,t2 
sw t1,-16(sp)
L92: 
lw t1,-16(sp)
sw t1,-12(sp)
L93: 
L94: 
lw t1,-20(sp)
li t2,0
beq ,t1, t2, L96
L95: 
j L99
L96: 
L97: 
lw t1,-24(sp)
li t2,0
bne ,t1, t2, L102
L98: 
j L99
L99: 
L100: 
lw t1,-28(sp)
li t2,0
beq ,t1, t2, L102
L101: 
j L104
L102: 
li t1,1
lw t0, -8(sp)
sw t1, 0(t0)
lw ra, 0(sp)
jr ra
L103: 
j L105
L104: 
li t1,0
lw t0, -8(sp)
sw t1, 0(t0)
lw ra, 0(sp)
jr ra
L105: 
lw ra,(sp)
jr ra
