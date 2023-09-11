public class Memoria {

    private int capacidade;

    public Memoria(int capacidade){
        this.capacidade = capacidade;
    }

    public void verifica_endereco(int ender) throws EnderecoInvalido {
        if ((ender < 0) || (ender >= capacidade)){
            throw new EnderecoInvalido(ender);
        }
    }

    public int getCapacidade(){
        return capacidade;
    }

    public int read(int ender) throws EnderecoInvalido {
        return 0;
    }

    public void write(int ender, int val) throws EnderecoInvalido {

    }
}
