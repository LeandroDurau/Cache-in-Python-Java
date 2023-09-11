public class EnderecoInvalido extends Exception{

    private int ender;

    public EnderecoInvalido(int ender){
        this.ender = ender;
    }

    @Override
    public String toString() {
        return String.valueOf(ender);
    }
}
