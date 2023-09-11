public class Cache extends Memoria{

    private int[] memoria;
    private RAM ram;
    private int inicio;

    public Cache(int capacidade, RAM ram) {
        super(capacidade);
        this.memoria = new int[this.getCapacidade()];
        this.inicio = ram.getCapacidade() + 1;
        this.ram = ram;
    }

    @Override
    public int read(int ender) throws EnderecoInvalido {
        if ((ender < inicio) || (ender >= inicio + this.getCapacidade())){
            System.out.println("Cache Miss: " + String.valueOf(ender));
            ram.verifica_endereco(ender);
            for (int i=0; i < this.getCapacidade(); i++){
                if (inicio != ram.getCapacidade() + 1){
                    ram.write(inicio + i, memoria[i]);
                }
                memoria[i] = ram.read(ender + i);
            }
            inicio = ender;
        }else System.out.println("Cache Hit: " +String.valueOf(ender));
        return memoria[ender - inicio];
    }

    @Override
    public void write(int ender, int val) throws EnderecoInvalido {
        if ((ender < inicio) || (ender >= inicio + this.getCapacidade())){
            System.out.println("Cache Miss " + String.valueOf(ender));
            ram.verifica_endereco(ender);
            for (int i=0; i < this.getCapacidade(); i++){
                if (inicio != ram.getCapacidade()+1){
                    ram.write(inicio + i, memoria[i]);
                }
                memoria [i] = ram.read(ender + i);
            }
            inicio = ender;
        }else  System.out.println("Cache Hit: " + String.valueOf(ender));
        memoria[ender - inicio] = val;
    }
}
