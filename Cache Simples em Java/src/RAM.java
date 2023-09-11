public class RAM extends Memoria{

    private int[] memoria;

    public RAM(int capacidade) {
        super((int) Math.pow(2,capacidade));
        memoria = new int[this.getCapacidade()];
    }

    @Override
    public int read(int ender) throws EnderecoInvalido {
        this.verifica_endereco(ender);
        return memoria[ender];
    }

    @Override
    public void write(int ender, int val) throws EnderecoInvalido {
        this.verifica_endereco(ender);
        memoria[ender] = val;
    }
}
