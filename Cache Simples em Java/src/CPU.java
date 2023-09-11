public class CPU {
    private Memoria mem;
    private IO io;
    private int PC;
    private int A;
    private int B;
    private int C;

    public CPU(Memoria mem, IO io){
        this.mem = mem;
        this.io = io;
        this.PC = 0;
        this.A = this.B = this.C = 0;
    }

    public void run(int ender) throws EnderecoInvalido {
        PC = ender;
        A = mem.read(PC);
        PC += 1;
        B = mem.read(PC);
        PC += 1;
        C = 1;
        while (A <= B){
            mem.write(A, C);
            io.output("> " + String.valueOf(A) + " = " + String.valueOf(C));
            C += 1;
            A += 1;
        }
    }

}
