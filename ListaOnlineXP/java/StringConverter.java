/* ----------------------------------------------- *
 *				Marco Aurélio Gerosa               *
 * ----------------------------------------------- *

 Histórico de Versões
 --------------------
 Versão	Autor		Modificação
 ------	-----		-----------
 1.0	Gerosa 		Importação e adaptação da classe
 * 
 */

public class StringConverter {
	

public static String concatenateWithoutRepetion(String palavra, String str) throws Exception {

	if ((palavra == null) || palavra.equals("")) {
		return str;
	} 
	
	if ((str == null) || str.equals("")) {
		return palavra;
	} 

	if ((str.startsWith(inicialMinuscula(palavra))) || (str.startsWith(inicialMaiuscula(palavra)))) {
		return str;
	}

	return palavra+" "+str;
	
}
public static String convertSpaces(String aString) throws Exception {
	String returnStr = aString;
	StringChanger strChange = new StringChanger();

	if (returnStr == null)
		returnStr = "";

	else
		returnStr = strChange.changeSubstring(returnStr, " ", "%20");

	return returnStr;

}
/**
 * fromDataBaseNotation method
 *
 * changes the Html &; notation (used just to store in DB)
 * to special letters of an input string
 *
 * @return java.lang.String
 * @param aString java.lang.String	input string
 */
public static String fromDataBaseNotation(String aString) throws Exception {
	String returnStr = aString;
	StringChanger strChange = new StringChanger();

	if (returnStr == null)
		returnStr = "";

	else
	{

		returnStr = strChange.changeSubstring(returnStr, "&#39;", "'");
		returnStr = strChange.changeSubstring(returnStr, "&#63;", "?");
		returnStr = strChange.changeSubstring(returnStr, "&quot;", "\"");
	}

	return returnStr;
}
/**
 * This method was created in VisualAge.
 * @return java.lang.String
 * @param aString java.lang.String
 */
public static String fromHtmlNotation(String aString) throws Exception {
	String returnStr = aString;
	StringChanger strChange = new StringChanger();

	if (returnStr == null)
		returnStr = "";

	else
	{
		returnStr = strChange.changeSubstring(returnStr, "&agrave;", "à");
		returnStr = strChange.changeSubstring(returnStr, "&aacute;", "á");
		returnStr = strChange.changeSubstring(returnStr, "&acirc;", "â");
		returnStr = strChange.changeSubstring(returnStr, "&atilde;", "ã");
		returnStr = strChange.changeSubstring(returnStr, "&auml;", "ä");
		returnStr = strChange.changeSubstring(returnStr, "&egrave;", "è");
		returnStr = strChange.changeSubstring(returnStr, "&eacute;", "é");
		returnStr = strChange.changeSubstring(returnStr, "&ecirc;", "ê");
		returnStr = strChange.changeSubstring(returnStr, "&euml;", "ë");
		returnStr = strChange.changeSubstring(returnStr, "&igrave;", "ì");
		returnStr = strChange.changeSubstring(returnStr, "&iacute;", "í");
		returnStr = strChange.changeSubstring(returnStr, "&icirc;", "î");
		returnStr = strChange.changeSubstring(returnStr, "&iuml;", "ï");
		returnStr = strChange.changeSubstring(returnStr, "&ograve;", "ò");
		returnStr = strChange.changeSubstring(returnStr, "&oacute;", "ó");
		returnStr = strChange.changeSubstring(returnStr, "&ocirc;", "ô");
		returnStr = strChange.changeSubstring(returnStr, "&otilde;", "õ");
		returnStr = strChange.changeSubstring(returnStr, "&ouml;", "ö");
		returnStr = strChange.changeSubstring(returnStr, "&ugrave;", "ù");
		returnStr = strChange.changeSubstring(returnStr, "&uacute;", "ú");
		returnStr = strChange.changeSubstring(returnStr, "&ucirc;", "û");
		returnStr = strChange.changeSubstring(returnStr, "&uuml;", "ü");
		returnStr = strChange.changeSubstring(returnStr, "&#39;", "'");
		returnStr = strChange.changeSubstring(returnStr, "&#63;", "?");
		returnStr = strChange.changeSubstring(returnStr, "&Agrave;", "À");
		returnStr = strChange.changeSubstring(returnStr, "&Aacute;", "Á");
		returnStr = strChange.changeSubstring(returnStr, "&Acirc;", "Â");
		returnStr = strChange.changeSubstring(returnStr, "&Atilde;", "Ã");
		returnStr = strChange.changeSubstring(returnStr, "&Auml;", "Ä");
		returnStr = strChange.changeSubstring(returnStr, "&Egrave;", "È");
		returnStr = strChange.changeSubstring(returnStr, "&Eacute;", "É");
		returnStr = strChange.changeSubstring(returnStr, "&Ecirc;", "Ê");
		returnStr = strChange.changeSubstring(returnStr, "&Euml;", "Ë");
		returnStr = strChange.changeSubstring(returnStr, "&Igrave;", "Ì");
		returnStr = strChange.changeSubstring(returnStr, "&Iacute;", "Í");
		returnStr = strChange.changeSubstring(returnStr, "&Icirc;", "Î");
		returnStr = strChange.changeSubstring(returnStr, "&Iuml;", "Ï");
		returnStr = strChange.changeSubstring(returnStr, "&Ograve;", "Ò");
		returnStr = strChange.changeSubstring(returnStr, "&Oacute;", "Ó");
		returnStr = strChange.changeSubstring(returnStr, "&Ocirc;", "Ô");
		returnStr = strChange.changeSubstring(returnStr, "&Otilde;", "Õ");
		returnStr = strChange.changeSubstring(returnStr, "&Ouml;", "Ö");
		returnStr = strChange.changeSubstring(returnStr, "&Ugrave;", "Ù");
		returnStr = strChange.changeSubstring(returnStr, "&Uacute;", "Ú");
		returnStr = strChange.changeSubstring(returnStr, "&Ucirc;", "Û");
		returnStr = strChange.changeSubstring(returnStr, "&Uuml;", "Ü");
		returnStr = strChange.changeSubstring(returnStr, "&ccedil;", "ç");
		returnStr = strChange.changeSubstring(returnStr, "&Ccedil;", "Ç");
		returnStr = strChange.changeSubstring(returnStr, "&#124;", "|");
		returnStr = strChange.changeSubstring(returnStr, "&#63;", "?");
		returnStr = strChange.changeSubstring(returnStr, "&quot;", "\"");
		returnStr = strChange.changeSubstring(returnStr, "&#39;", "'");
		returnStr = strChange.changeSubstring(returnStr, "<br>", "\n");
	}

	return returnStr;
}
/**
 * This method was created in VisualAge.
 * @return java.lang.String
 * @param aString java.lang.String
 */
public static String fromHtmlNotationWithoutLineBreak(String aString) throws Exception {
	String returnStr = aString;
	StringChanger strChange = new StringChanger();

	if (returnStr == null)
		returnStr = "";

	else
	{
		returnStr = strChange.changeSubstring(returnStr, "&agrave;", "à");
		returnStr = strChange.changeSubstring(returnStr, "&aacute;", "á");
		returnStr = strChange.changeSubstring(returnStr, "&acirc;", "â");
		returnStr = strChange.changeSubstring(returnStr, "&atilde;", "ã");
		returnStr = strChange.changeSubstring(returnStr, "&auml;", "ä");
		returnStr = strChange.changeSubstring(returnStr, "&egrave;", "è");
		returnStr = strChange.changeSubstring(returnStr, "&eacute;", "é");
		returnStr = strChange.changeSubstring(returnStr, "&ecirc;", "ê");
		returnStr = strChange.changeSubstring(returnStr, "&euml;", "ë");
		returnStr = strChange.changeSubstring(returnStr, "&igrave;", "ì");
		returnStr = strChange.changeSubstring(returnStr, "&iacute;", "í");
		returnStr = strChange.changeSubstring(returnStr, "&icirc;", "î");
		returnStr = strChange.changeSubstring(returnStr, "&iuml;", "ï");
		returnStr = strChange.changeSubstring(returnStr, "&ograve;", "ò");
		returnStr = strChange.changeSubstring(returnStr, "&oacute;", "ó");
		returnStr = strChange.changeSubstring(returnStr, "&ocirc;", "ô");
		returnStr = strChange.changeSubstring(returnStr, "&otilde;", "õ");
		returnStr = strChange.changeSubstring(returnStr, "&ouml;", "ö");
		returnStr = strChange.changeSubstring(returnStr, "&ugrave;", "ù");
		returnStr = strChange.changeSubstring(returnStr, "&uacute;", "ú");
		returnStr = strChange.changeSubstring(returnStr, "&ucirc;", "û");
		returnStr = strChange.changeSubstring(returnStr, "&uuml;", "ü");
		returnStr = strChange.changeSubstring(returnStr, "&#39;", "'");
		returnStr = strChange.changeSubstring(returnStr, "&#63;", "?");
		returnStr = strChange.changeSubstring(returnStr, "&Agrave;", "À");
		returnStr = strChange.changeSubstring(returnStr, "&Aacute;", "Á");
		returnStr = strChange.changeSubstring(returnStr, "&Acirc;", "Â");
		returnStr = strChange.changeSubstring(returnStr, "&Atilde;", "Ã");
		returnStr = strChange.changeSubstring(returnStr, "&Auml;", "Ä");
		returnStr = strChange.changeSubstring(returnStr, "&Egrave;", "È");
		returnStr = strChange.changeSubstring(returnStr, "&Eacute;", "É");
		returnStr = strChange.changeSubstring(returnStr, "&Ecirc;", "Ê");
		returnStr = strChange.changeSubstring(returnStr, "&Euml;", "Ë");
		returnStr = strChange.changeSubstring(returnStr, "&Igrave;", "Ì");
		returnStr = strChange.changeSubstring(returnStr, "&Iacute;", "Í");
		returnStr = strChange.changeSubstring(returnStr, "&Icirc;", "Î");
		returnStr = strChange.changeSubstring(returnStr, "&Iuml;", "Ï");
		returnStr = strChange.changeSubstring(returnStr, "&Ograve;", "Ò");
		returnStr = strChange.changeSubstring(returnStr, "&Oacute;", "Ó");
		returnStr = strChange.changeSubstring(returnStr, "&Ocirc;", "Ô");
		returnStr = strChange.changeSubstring(returnStr, "&Otilde;", "Õ");
		returnStr = strChange.changeSubstring(returnStr, "&Ouml;", "Ö");
		returnStr = strChange.changeSubstring(returnStr, "&Ugrave;", "Ù");
		returnStr = strChange.changeSubstring(returnStr, "&Uacute;", "Ú");
		returnStr = strChange.changeSubstring(returnStr, "&Ucirc;", "Û");
		returnStr = strChange.changeSubstring(returnStr, "&Uuml;", "Ü");
		returnStr = strChange.changeSubstring(returnStr, "&ccedil;", "ç");
		returnStr = strChange.changeSubstring(returnStr, "&Ccedil;", "Ç");
		returnStr = strChange.changeSubstring(returnStr, "&#124;", "|");
		returnStr = strChange.changeSubstring(returnStr, "&#63;", "?");
		returnStr = strChange.changeSubstring(returnStr, "&quot;", "\"");
		returnStr = strChange.changeSubstring(returnStr, "&#39;", "'");
//		returnStr = strChange.changeSubstring(returnStr, "<br>", "\n");
	}

	return returnStr;
}
// Coloca a inicial de uma string em letra maiúscula

public static String inicialMaiuscula(String str) throws Exception {

	if (str == null) return null;

	if (str.equals("")) return "";

	return str.substring(0,1).toUpperCase() + str.substring(1);
	
}
// Coloca a inicial de uma string em letra minuscula

public static String inicialMinuscula(String str) throws Exception {

	if (str == null) return null;

	if (str.equals("")) return "";

	return str.substring(0,1).toLowerCase() + str.substring(1);
	
}


public static String removeAcentos(String aString) throws Exception {
	String returnStr = new String (aString);
	StringChanger strChange = new StringChanger();

	if (returnStr == null) {
		returnStr = "";
	} else {
		
		returnStr = strChange.changeSubstring(returnStr, "à", "a");
		returnStr = strChange.changeSubstring(returnStr, "á", "a");
		returnStr = strChange.changeSubstring(returnStr, "â", "a");
		returnStr = strChange.changeSubstring(returnStr, "ã", "a");
		returnStr = strChange.changeSubstring(returnStr, "ä", "a");
		returnStr = strChange.changeSubstring(returnStr, "è", "e");
		returnStr = strChange.changeSubstring(returnStr, "é", "e");
		returnStr = strChange.changeSubstring(returnStr, "ê", "e");
		returnStr = strChange.changeSubstring(returnStr, "ë", "e");
		returnStr = strChange.changeSubstring(returnStr, "ì", "i");
		returnStr = strChange.changeSubstring(returnStr, "í", "i");
		returnStr = strChange.changeSubstring(returnStr, "î", "i");
		returnStr = strChange.changeSubstring(returnStr, "ï", "i");
		returnStr = strChange.changeSubstring(returnStr, "ò", "o");
		returnStr = strChange.changeSubstring(returnStr, "ó", "o");
		returnStr = strChange.changeSubstring(returnStr, "ô", "o");
		returnStr = strChange.changeSubstring(returnStr, "õ", "o");
		returnStr = strChange.changeSubstring(returnStr, "ö", "o");
		returnStr = strChange.changeSubstring(returnStr, "ù", "u");
		returnStr = strChange.changeSubstring(returnStr, "ú", "u");
		returnStr = strChange.changeSubstring(returnStr, "û", "u");
		returnStr = strChange.changeSubstring(returnStr, "ü", "u");
		returnStr = strChange.changeSubstring(returnStr, "À", "A");
		returnStr = strChange.changeSubstring(returnStr, "Á", "A");
		returnStr = strChange.changeSubstring(returnStr, "Â", "A");
		returnStr = strChange.changeSubstring(returnStr, "Ã", "A");
		returnStr = strChange.changeSubstring(returnStr, "Ä", "A");
		returnStr = strChange.changeSubstring(returnStr, "È", "E");
		returnStr = strChange.changeSubstring(returnStr, "É", "E");
		returnStr = strChange.changeSubstring(returnStr, "Ê", "E");
		returnStr = strChange.changeSubstring(returnStr, "Ë", "E");
		returnStr = strChange.changeSubstring(returnStr, "Ì", "I");
		returnStr = strChange.changeSubstring(returnStr, "Í", "I");
		returnStr = strChange.changeSubstring(returnStr, "Î", "I");
		returnStr = strChange.changeSubstring(returnStr, "Ï", "I");
		returnStr = strChange.changeSubstring(returnStr, "Ò", "O");
		returnStr = strChange.changeSubstring(returnStr, "Ó", "O");
		returnStr = strChange.changeSubstring(returnStr, "Ô", "O");
		returnStr = strChange.changeSubstring(returnStr, "Õ", "O");
		returnStr = strChange.changeSubstring(returnStr, "Ö", "O");
		returnStr = strChange.changeSubstring(returnStr, "Ù", "U");
		returnStr = strChange.changeSubstring(returnStr, "Ú", "U");
		returnStr = strChange.changeSubstring(returnStr, "Û", "U");
		returnStr = strChange.changeSubstring(returnStr, "Ü", "U");
		returnStr = strChange.changeSubstring(returnStr, "ç", "c");
		returnStr = strChange.changeSubstring(returnStr, "Ç", "C");
	}

	return returnStr;
}
public static String removeUnecessarySpaces(String aString) throws Exception {

	String returnStr = aString;
	StringChanger strChange = new StringChanger();

	if (returnStr == null) return "";

	while (returnStr.indexOf("  ") != -1) {
		returnStr = strChange.changeSubstring(returnStr, "  ", " ");
	}

	while (returnStr.startsWith(" ")) {
		returnStr = returnStr.substring(1,returnStr.length());
	}

	while (returnStr.endsWith(" ")) {
		returnStr = returnStr.substring(0,returnStr.length()-1);
	}
	
	return returnStr;

}

public static String replace(String aString, String txtToFind, String txtToReplace) throws Exception {

	String returnStr = aString;
	StringChanger strChange = new StringChanger();

	if (returnStr == null) returnStr = "";

	returnStr = strChange.changeSubstring(returnStr, txtToFind,txtToReplace);

	return returnStr;
}
/**
 * toDataBaseNotation method
 *
 * changes the special letters of an input string
 * to Html &; notation (just to store in DB)
 *
 * @return java.lang.String
 * @param aString java.lang.String	input string
 */
public static String toDataBaseNotation(String aString) throws Exception {
	String returnStr = aString;
	StringChanger strChange = new StringChanger();

	if (returnStr == null)
		returnStr = "";

	else
	{

		char c[] = new char[1];
		c[0] = 147; // abre aspas do word
		returnStr = strChange.changeSubstring(returnStr, new String(c), "\"");
		c[0] = 148; // fecha aspas do word
		returnStr = strChange.changeSubstring(returnStr, new String(c), "\"");
		returnStr = strChange.changeSubstring(returnStr, "'", "&#39;");
		returnStr = strChange.changeSubstring(returnStr, "?", "&#63;");
		returnStr = strChange.changeSubstring(returnStr, "\"", "&quot;");
	}

	return returnStr;
}
/**
 * toHtmlNotation method
 *
 * changes the stressed and the special letters of an input string
 * to Html &; notation
 *
 * @return java.lang.String
 * @param aString java.lang.String	input string
 */
public static String toHtmlNotation(String aString) throws Exception {
	String returnStr = aString;
	StringChanger strChange = new StringChanger();

	if (returnStr == null)
		returnStr = "";

	else
	{
		// Altera os amps existentes para nao confundir com os acrescentados
		returnStr = strChange.changeSubstring(returnStr, "&", "&amp;");
		// Troca os caracteres por seus correspondentes
		returnStr = strChange.changeSubstring(returnStr, "à", "&agrave;");
		returnStr = strChange.changeSubstring(returnStr, "á", "&aacute;");
		returnStr = strChange.changeSubstring(returnStr, "â", "&acirc;");
		returnStr = strChange.changeSubstring(returnStr, "ã", "&atilde;");
		returnStr = strChange.changeSubstring(returnStr, "ä", "&auml;");
		returnStr = strChange.changeSubstring(returnStr, "è", "&egrave;");
		returnStr = strChange.changeSubstring(returnStr, "é", "&eacute;");
		returnStr = strChange.changeSubstring(returnStr, "ê", "&ecirc;");
		returnStr = strChange.changeSubstring(returnStr, "ë", "&euml;");
		returnStr = strChange.changeSubstring(returnStr, "ì", "&igrave;");
		returnStr = strChange.changeSubstring(returnStr, "í", "&iacute;");
		returnStr = strChange.changeSubstring(returnStr, "î", "&icirc;");
		returnStr = strChange.changeSubstring(returnStr, "ï", "&iuml;");
		returnStr = strChange.changeSubstring(returnStr, "ò", "&ograve;");
		returnStr = strChange.changeSubstring(returnStr, "ó", "&oacute;");
		returnStr = strChange.changeSubstring(returnStr, "ô", "&ocirc;");
		returnStr = strChange.changeSubstring(returnStr, "õ", "&otilde;");
		returnStr = strChange.changeSubstring(returnStr, "ö", "&ouml;");
		returnStr = strChange.changeSubstring(returnStr, "ù", "&ugrave;");
		returnStr = strChange.changeSubstring(returnStr, "ú", "&uacute;");
		returnStr = strChange.changeSubstring(returnStr, "û", "&ucirc;");
		returnStr = strChange.changeSubstring(returnStr, "ü", "&uuml;");
		returnStr = strChange.changeSubstring(returnStr, "À", "&Agrave;");
		returnStr = strChange.changeSubstring(returnStr, "Á", "&Aacute;");
		returnStr = strChange.changeSubstring(returnStr, "Â", "&Acirc;");
		returnStr = strChange.changeSubstring(returnStr, "Ã", "&Atilde;");
		returnStr = strChange.changeSubstring(returnStr, "Ä", "&Auml;");
		returnStr = strChange.changeSubstring(returnStr, "È", "&Egrave;");
		returnStr = strChange.changeSubstring(returnStr, "É", "&Eacute;");
		returnStr = strChange.changeSubstring(returnStr, "Ê", "&Ecirc;");
		returnStr = strChange.changeSubstring(returnStr, "Ë", "&Euml;");
		returnStr = strChange.changeSubstring(returnStr, "Ì", "&Igrave;");
		returnStr = strChange.changeSubstring(returnStr, "Í", "&Iacute;");
		returnStr = strChange.changeSubstring(returnStr, "Î", "&Icirc;");
		returnStr = strChange.changeSubstring(returnStr, "Ï", "&Iuml;");
		returnStr = strChange.changeSubstring(returnStr, "Ò", "&Ograve;");
		returnStr = strChange.changeSubstring(returnStr, "Ó", "&Oacute;");
		returnStr = strChange.changeSubstring(returnStr, "Ô", "&Ocirc;");
		returnStr = strChange.changeSubstring(returnStr, "Õ", "&Otilde;");
		returnStr = strChange.changeSubstring(returnStr, "Ö", "&Ouml;");
		returnStr = strChange.changeSubstring(returnStr, "Ù", "&Ugrave;");
		returnStr = strChange.changeSubstring(returnStr, "Ú", "&Uacute;");
		returnStr = strChange.changeSubstring(returnStr, "Û", "&Ucirc;");
		returnStr = strChange.changeSubstring(returnStr, "Ü", "&Uuml;");
		returnStr = strChange.changeSubstring(returnStr, "ç", "&ccedil;");
		returnStr = strChange.changeSubstring(returnStr, "Ç", "&Ccedil;");
		returnStr = strChange.changeSubstring(returnStr, "'", "&#39;");
		returnStr = strChange.changeSubstring(returnStr, "?", "&#63;");
		returnStr = strChange.changeSubstring(returnStr, "|", "&#124;");
		returnStr = strChange.changeSubstring(returnStr, "\"", "&quot;");
		returnStr = strChange.changeSubstring(returnStr, "'", "&#39;");
		returnStr = strChange.changeSubstring(returnStr, "\r", "");
		returnStr = strChange.changeSubstring(returnStr, "<", "&lt;");
		returnStr = strChange.changeSubstring(returnStr, ">", "&gt;");
		// troca os caracteres por tags correspondentes
		returnStr = strChange.changeSubstring(returnStr, "\n", "<br>");
	}

	return returnStr;
}
/**
 * toHtmlNotation method
 *
 * changes the [\n] caracter to [\n" + "] string to avoid the "Unterminated string constant"
 * JavaScript error
 *
 * @return java.lang.String
 * @param aString java.lang.String	input string
 */
public static String toJavaScriptNotation(String aString) throws Exception {
	String returnStr = aString;
	StringChanger strChange = new StringChanger();

	if (returnStr == null)
		returnStr = "";
	else
	{
		returnStr = strChange.changeSubstring(returnStr, "\r", "");
		returnStr = strChange.changeSubstring(returnStr, "\n", "\\n");
		returnStr = strChange.changeSubstring(returnStr, "\"", "\\\"");
		returnStr = strChange.changeSubstring(returnStr, "'", "\\'");
	}

	return returnStr;
}
/**
 * toUnStressedNotation method
 *
 * changes the stressed, the special letters and the Html &; notation
 * to unstressed letters in an input string
 *
 * @return java.lang.String
 * @param aString java.lang.String	input string
 */
public static String toUnStressedNotation(String aString) throws Exception {
	String returnStr = aString;
	StringChanger strChange = new StringChanger();

	if (returnStr == null)
		returnStr = "";

	else
	{
		returnStr = strChange.changeSubstring(returnStr, "&agrave;", "a");
		returnStr = strChange.changeSubstring(returnStr, "à", "a");
		returnStr = strChange.changeSubstring(returnStr, "&aacute;", "a");
		returnStr = strChange.changeSubstring(returnStr, "á", "a");
		returnStr = strChange.changeSubstring(returnStr, "&acirc;",  "a");
		returnStr = strChange.changeSubstring(returnStr, "â",  "a");
		returnStr = strChange.changeSubstring(returnStr, "&atilde;", "a");
		returnStr = strChange.changeSubstring(returnStr, "ã", "a");
		returnStr = strChange.changeSubstring(returnStr, "&auml;", "a");
		returnStr = strChange.changeSubstring(returnStr, "ä", "a");
		returnStr = strChange.changeSubstring(returnStr, "&egrave;", "e");
		returnStr = strChange.changeSubstring(returnStr, "è", "e");
		returnStr = strChange.changeSubstring(returnStr, "&eacute;", "e");
		returnStr = strChange.changeSubstring(returnStr, "é", "e");
		returnStr = strChange.changeSubstring(returnStr, "&ecirc;", "e");
		returnStr = strChange.changeSubstring(returnStr, "ê", "e");
		returnStr = strChange.changeSubstring(returnStr, "&euml;", "e");
		returnStr = strChange.changeSubstring(returnStr, "ë", "e");
		returnStr = strChange.changeSubstring(returnStr, "&igrave;", "i");
		returnStr = strChange.changeSubstring(returnStr, "ì", "i");
		returnStr = strChange.changeSubstring(returnStr, "&iacute;", "i");
		returnStr = strChange.changeSubstring(returnStr, "í", "i");
		returnStr = strChange.changeSubstring(returnStr, "&icirc;", "i");
		returnStr = strChange.changeSubstring(returnStr, "î", "i");
		returnStr = strChange.changeSubstring(returnStr, "&iuml;", "i");
		returnStr = strChange.changeSubstring(returnStr, "ï", "i");
		returnStr = strChange.changeSubstring(returnStr, "&ograve;", "o");
		returnStr = strChange.changeSubstring(returnStr, "ò", "o");
		returnStr = strChange.changeSubstring(returnStr, "&oacute;", "o");
		returnStr = strChange.changeSubstring(returnStr, "ó", "o");
		returnStr = strChange.changeSubstring(returnStr, "&ocirc;", "o");
		returnStr = strChange.changeSubstring(returnStr, "ô", "o");
		returnStr = strChange.changeSubstring(returnStr, "&otilde;", "o");
		returnStr = strChange.changeSubstring(returnStr, "õ", "o");
		returnStr = strChange.changeSubstring(returnStr, "&ouml;", "o");
		returnStr = strChange.changeSubstring(returnStr, "ö", "o");
		returnStr = strChange.changeSubstring(returnStr, "&ugrave;", "u");
		returnStr = strChange.changeSubstring(returnStr, "ù", "u");
		returnStr = strChange.changeSubstring(returnStr, "&uacute;", "u");
		returnStr = strChange.changeSubstring(returnStr, "ú", "u");
		returnStr = strChange.changeSubstring(returnStr, "&ucirc;", "u");
		returnStr = strChange.changeSubstring(returnStr, "û", "u");
		returnStr = strChange.changeSubstring(returnStr, "&uuml;", "u");
		returnStr = strChange.changeSubstring(returnStr, "ü", "u");
		returnStr = strChange.changeSubstring(returnStr, "'", "");
		returnStr = strChange.changeSubstring(returnStr, "?", "");
		returnStr = strChange.changeSubstring(returnStr, "&Agrave;", "A");
		returnStr = strChange.changeSubstring(returnStr, "À", "A");
		returnStr = strChange.changeSubstring(returnStr, "&Aacute;", "A");
		returnStr = strChange.changeSubstring(returnStr, "Á", "A");
		returnStr = strChange.changeSubstring(returnStr, "&Acirc;", "A");
		returnStr = strChange.changeSubstring(returnStr, "Â", "A");
		returnStr = strChange.changeSubstring(returnStr, "&Atilde;", "A");
		returnStr = strChange.changeSubstring(returnStr, "Ã", "A");
		returnStr = strChange.changeSubstring(returnStr, "&Auml;", "A");
		returnStr = strChange.changeSubstring(returnStr, "Ä", "A");
		returnStr = strChange.changeSubstring(returnStr, "&Egrave;", "E");
		returnStr = strChange.changeSubstring(returnStr, "È", "E");
		returnStr = strChange.changeSubstring(returnStr, "&Eacute;", "E");
		returnStr = strChange.changeSubstring(returnStr, "É", "E");
		returnStr = strChange.changeSubstring(returnStr, "&Ecirc;", "E");
		returnStr = strChange.changeSubstring(returnStr, "Ê", "E");
		returnStr = strChange.changeSubstring(returnStr, "&Euml;", "E");
		returnStr = strChange.changeSubstring(returnStr, "Ë", "E");
		returnStr = strChange.changeSubstring(returnStr, "&Igrave;", "I");
		returnStr = strChange.changeSubstring(returnStr, "Ì", "I");
		returnStr = strChange.changeSubstring(returnStr, "&Iacute;", "I");
		returnStr = strChange.changeSubstring(returnStr, "Í", "I");
		returnStr = strChange.changeSubstring(returnStr, "&Icirc;", "I");
		returnStr = strChange.changeSubstring(returnStr, "Î", "I");
		returnStr = strChange.changeSubstring(returnStr, "&Iuml;", "I");
		returnStr = strChange.changeSubstring(returnStr, "Ï", "I");
		returnStr = strChange.changeSubstring(returnStr, "&Ograve;", "O");
		returnStr = strChange.changeSubstring(returnStr, "Ò", "O");
		returnStr = strChange.changeSubstring(returnStr, "&Oacute;", "O");
		returnStr = strChange.changeSubstring(returnStr, "Ó", "O");
		returnStr = strChange.changeSubstring(returnStr, "&Ocirc;", "O");
		returnStr = strChange.changeSubstring(returnStr, "Ô", "O");
		returnStr = strChange.changeSubstring(returnStr, "&Otilde;", "O");
		returnStr = strChange.changeSubstring(returnStr, "Õ", "O");
		returnStr = strChange.changeSubstring(returnStr, "&Ouml;", "O");
		returnStr = strChange.changeSubstring(returnStr, "Ö", "O");
		returnStr = strChange.changeSubstring(returnStr, "&Ugrave;", "U");
		returnStr = strChange.changeSubstring(returnStr, "Ù", "U");
		returnStr = strChange.changeSubstring(returnStr, "&Uacute;", "U");
		returnStr = strChange.changeSubstring(returnStr, "Ú", "U");
		returnStr = strChange.changeSubstring(returnStr, "&Ucirc;", "U");
		returnStr = strChange.changeSubstring(returnStr, "Û", "U");
		returnStr = strChange.changeSubstring(returnStr, "&Uuml;", "U");
		returnStr = strChange.changeSubstring(returnStr, "Ü", "U");
		returnStr = strChange.changeSubstring(returnStr, "&ccedil;", "c");
		returnStr = strChange.changeSubstring(returnStr, "ç", "c");
		returnStr = strChange.changeSubstring(returnStr, "&Ccedil;", "C");
		returnStr = strChange.changeSubstring(returnStr, "Ç", "C");
		returnStr = strChange.changeSubstring(returnStr, "&#124;", "|");
		returnStr = strChange.changeSubstring(returnStr, "&#63;", "?");
		returnStr = strChange.changeSubstring(returnStr, "&quot;","\"");
		returnStr = strChange.changeSubstring(returnStr, "&#39;","'");
		returnStr = strChange.changeSubstring(returnStr, "<br>","\n");
	}

	return returnStr;
}
}
