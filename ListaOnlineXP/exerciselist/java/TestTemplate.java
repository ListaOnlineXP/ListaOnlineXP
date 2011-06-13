
public class RealizaTesteNaClasseSubmetida {

    public static void assertEquals(int valor, int expected, String txt) throws Exception {
        if (expected != valor) {
            throw new TestException("TEST_ERROR!:!Falha na execução.\n Para "+txt+" era esperado "+expected +", porém retornou "+valor+".");
        }
    }

    public static void assertEquals(long valor, long expected, String txt) throws Exception {
        if (expected != valor) {
            throw new TestException("TEST_ERROR!:!Falha na execução.\n Para "+txt+" era esperado "+expected +", porém retornou "+valor+".");
        }
    }

    public static void assertEquals(float valor, float expected, String txt) throws Exception {
        if (arredonda(expected,5) != arredonda(valor,5)) {
            throw new TestException("TEST_ERROR!:!Falha na execução.\n Para "+txt+" era esperado "+expected +", porém retornou "+valor+".");
        }
    }

    public static void assertEquals(double valor, double expected, String txt) throws Exception {
        if (arredonda(expected,5) != arredonda(valor,5)) {
            throw new TestException("TEST_ERROR!:!Falha na execução.\n Para "+txt+" era esperado "+expected +", porém retornou "+valor+".");
        }
    }

    public static double arredonda(double valor, int precisao) {
        return Math.round(valor * Math.pow(10,precisao) / (1.0 * Math.pow(10,precisao)));
    }

    public static void assertEquals(boolean valor, boolean expected, String txt) throws Exception {
        if (expected != valor) {
            throw new TestException("TEST_ERROR!:!Falha na execução.\n Para "+txt+" era esperado "+expected +", porém retornou "+valor+".");
        }
    }

    public static void assertEquals(Object valor, Object expected, String txt) throws Exception {
        if (expected == null) {
            if (valor != null) {
                throw new TestException("TEST_ERROR!:!Falha na execução.\n Para "+txt+" era esperado null, porém retornou \""+valor.toString()+"\".");
            }
        } else {
            if (!expected.equals(valor)) {
                throw new TestException("TEST_ERROR!:!Falha na execução.\n Para "+txt+" era esperado \""+expected.toString() +"\", porém retornou \""+valor.toString()+"\".");
            }
        }
    }

    public static void assertBetween(int valor, int liminf, int limsup, String txt) throws Exception {
        if (valor < liminf || valor > limsup) {
            throw new TestException("TEST_ERROR!:!Falha na execução.\n Para "+txt+" era esperado um valor entre "+liminf
                +" e "+limsup +", porém retornou "+valor+".");
        }
    }

    public static void assertTrue (boolean valor, String txt) throws Exception {
        if (!valor) {
            throw new TestException("TEST_ERROR!:!Falha na execução.\n Para "+txt+" era esperado true, porém retornou false.");
        }
    }


    public static void main(String[] args) {
        try {

            // Realiza os testes
            assertEquals(0, 0, "0");

            /* Insert code here */

            System.out.println("CORRECT!:!Executou corretamente. Parabéns!"); // Este texto é usado para detectar respostas corretas.
            System.err.println("CORRECT!:!Executou corretamente. Parabéns!"); // Este texto é usado para detectar respostas corretas.
            System.exit(0);

        } catch (TestException ex) {
            System.out.println(ex.getMessage());
            System.exit(1);
        } catch (Exception ex) {
            System.out.println("UNKNOWN_SYSTEM_ERROR!:!Ocorreu um erro desconhecido. Favor entrar em contato com o professor.");
            System.out.println("UNKNOWN_SYSTEM_ERROR_MESSAGE!:!"+ ex.getMessage());
            System.out.println("UNKNOWN_SYSTEM_ERROR_TYPE!:!" + ex.getClass());
            System.out.println("UNKNOWN_SYSTEM_ERROR_WHERE!:!"+ ex.getStackTrace()[0]);
            System.exit(1);
            //ex.printStackTrace(System.out);
            //ex.printStackTrace();
        }

    }
}

class TestException extends Exception {

    public TestException(String string) {
        super(string);
    }

}

