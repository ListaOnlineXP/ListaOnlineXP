import java.io.BufferedReader;
import java.io.File;
import java.io.FileReader;
import java.io.FileWriter;
import java.io.IOException;
import java.io.PrintWriter;

public class Compilar {

    public synchronized static String compilar(String path, String nomeClasse, String codigo)
            throws Exception {
        /* grava o codigo-fonte no disco */
        String arquivoFonte = nomeClasse + ".java";
        FileWriter arq = new FileWriter(path + arquivoFonte);
        arq.write(codigo); // grava no arquivo o codigo
        arq.close();

        return compilar(path, arquivoFonte);
    }

    public synchronized static String compilar(String path, String fileName) throws Exception {

        File file = new File(path+"logCompilacao.txt");
        if (file.exists()) file.delete();

        if (!(new File(path+fileName).exists())) throw new Exception("Arquivo "+fileName+" não encontrado.");
        
        /* deixa um log da compilacao num arquivo chamado logCompilacao.txt */
        PrintWriter saida = new PrintWriter(new FileWriter(path+"logCompilacao.txt"));
        StringBuffer txtResultados = new StringBuffer();
        
        int resultadoCompilacao = com.sun.tools.javac.Main.compile(
                new String[] { "-classpath", (new File(path)).getCanonicalPath(), path+fileName}, saida);
        saida.close();
        
        /* le o arquivo de resultados e imprime na tela */
        BufferedReader result = new BufferedReader(new FileReader(path+"logCompilacao.txt"));
        String linha;
        while ((linha = result.readLine()) != null) {
            txtResultados.append(linha + "\n");
        }

        return txtResultados.toString();
    }
}
