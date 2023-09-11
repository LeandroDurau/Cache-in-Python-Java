public class Main {
    public static void main(String[] args) {
        try {
            IO io = new IO();
            RAM ram = new RAM(7);
            Cache cache = new Cache(8, ram);
            CPU cpu = new CPU(cache, io);

            int inicio = 10;
            ram.write(inicio, 118);
            ram.write(inicio + 1, 130);
            cpu.run(inicio);
        } catch (EnderecoInvalido e) {
            System.out.println("Endereço inválido: " + e.toString());
        }
    }

}
