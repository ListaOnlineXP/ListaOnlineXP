/* ----------------------------------------------- *
 *				Marco Aurйlio Gerosa               *
 * ----------------------------------------------- *

 Histуrico de Versхes
 --------------------
 Versгo	Autor		Modificaзгo
 ------	-----		-----------
 1.0	Gerosa 		Importaзгo e adaptaзгo da classe
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
		returnStr = strChange.changeSubstring(returnStr, "&agrave;", "а");
		returnStr = strChange.changeSubstring(returnStr, "&aacute;", "б");
		returnStr = strChange.changeSubstring(returnStr, "&acirc;", "в");
		returnStr = strChange.changeSubstring(returnStr, "&atilde;", "г");
		returnStr = strChange.changeSubstring(returnStr, "&auml;", "д");
		returnStr = strChange.changeSubstring(returnStr, "&egrave;", "и");
		returnStr = strChange.changeSubstring(returnStr, "&eacute;", "й");
		returnStr = strChange.changeSubstring(returnStr, "&ecirc;", "к");
		returnStr = strChange.changeSubstring(returnStr, "&euml;", "л");
		returnStr = strChange.changeSubstring(returnStr, "&igrave;", "м");
		returnStr = strChange.changeSubstring(returnStr, "&iacute;", "н");
		returnStr = strChange.changeSubstring(returnStr, "&icirc;", "о");
		returnStr = strChange.changeSubstring(returnStr, "&iuml;", "п");
		returnStr = strChange.changeSubstring(returnStr, "&ograve;", "т");
		returnStr = strChange.changeSubstring(returnStr, "&oacute;", "у");
		returnStr = strChange.changeSubstring(returnStr, "&ocirc;", "ф");
		returnStr = strChange.changeSubstring(returnStr, "&otilde;", "х");
		returnStr = strChange.changeSubstring(returnStr, "&ouml;", "ц");
		returnStr = strChange.changeSubstring(returnStr, "&ugrave;", "щ");
		returnStr = strChange.changeSubstring(returnStr, "&uacute;", "ъ");
		returnStr = strChange.changeSubstring(returnStr, "&ucirc;", "ы");
		returnStr = strChange.changeSubstring(returnStr, "&uuml;", "ь");
		returnStr = strChange.changeSubstring(returnStr, "&#39;", "'");
		returnStr = strChange.changeSubstring(returnStr, "&#63;", "?");
		returnStr = strChange.changeSubstring(returnStr, "&Agrave;", "А");
		returnStr = strChange.changeSubstring(returnStr, "&Aacute;", "Б");
		returnStr = strChange.changeSubstring(returnStr, "&Acirc;", "В");
		returnStr = strChange.changeSubstring(returnStr, "&Atilde;", "Г");
		returnStr = strChange.changeSubstring(returnStr, "&Auml;", "Д");
		returnStr = strChange.changeSubstring(returnStr, "&Egrave;", "И");
		returnStr = strChange.changeSubstring(returnStr, "&Eacute;", "Й");
		returnStr = strChange.changeSubstring(returnStr, "&Ecirc;", "К");
		returnStr = strChange.changeSubstring(returnStr, "&Euml;", "Л");
		returnStr = strChange.changeSubstring(returnStr, "&Igrave;", "М");
		returnStr = strChange.changeSubstring(returnStr, "&Iacute;", "Н");
		returnStr = strChange.changeSubstring(returnStr, "&Icirc;", "О");
		returnStr = strChange.changeSubstring(returnStr, "&Iuml;", "П");
		returnStr = strChange.changeSubstring(returnStr, "&Ograve;", "Т");
		returnStr = strChange.changeSubstring(returnStr, "&Oacute;", "У");
		returnStr = strChange.changeSubstring(returnStr, "&Ocirc;", "Ф");
		returnStr = strChange.changeSubstring(returnStr, "&Otilde;", "Х");
		returnStr = strChange.changeSubstring(returnStr, "&Ouml;", "Ц");
		returnStr = strChange.changeSubstring(returnStr, "&Ugrave;", "Щ");
		returnStr = strChange.changeSubstring(returnStr, "&Uacute;", "Ъ");
		returnStr = strChange.changeSubstring(returnStr, "&Ucirc;", "Ы");
		returnStr = strChange.changeSubstring(returnStr, "&Uuml;", "Ь");
		returnStr = strChange.changeSubstring(returnStr, "&ccedil;", "з");
		returnStr = strChange.changeSubstring(returnStr, "&Ccedil;", "З");
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
		returnStr = strChange.changeSubstring(returnStr, "&agrave;", "а");
		returnStr = strChange.changeSubstring(returnStr, "&aacute;", "б");
		returnStr = strChange.changeSubstring(returnStr, "&acirc;", "в");
		returnStr = strChange.changeSubstring(returnStr, "&atilde;", "г");
		returnStr = strChange.changeSubstring(returnStr, "&auml;", "д");
		returnStr = strChange.changeSubstring(returnStr, "&egrave;", "и");
		returnStr = strChange.changeSubstring(returnStr, "&eacute;", "й");
		returnStr = strChange.changeSubstring(returnStr, "&ecirc;", "к");
		returnStr = strChange.changeSubstring(returnStr, "&euml;", "л");
		returnStr = strChange.changeSubstring(returnStr, "&igrave;", "м");
		returnStr = strChange.changeSubstring(returnStr, "&iacute;", "н");
		returnStr = strChange.changeSubstring(returnStr, "&icirc;", "о");
		returnStr = strChange.changeSubstring(returnStr, "&iuml;", "п");
		returnStr = strChange.changeSubstring(returnStr, "&ograve;", "т");
		returnStr = strChange.changeSubstring(returnStr, "&oacute;", "у");
		returnStr = strChange.changeSubstring(returnStr, "&ocirc;", "ф");
		returnStr = strChange.changeSubstring(returnStr, "&otilde;", "х");
		returnStr = strChange.changeSubstring(returnStr, "&ouml;", "ц");
		returnStr = strChange.changeSubstring(returnStr, "&ugrave;", "щ");
		returnStr = strChange.changeSubstring(returnStr, "&uacute;", "ъ");
		returnStr = strChange.changeSubstring(returnStr, "&ucirc;", "ы");
		returnStr = strChange.changeSubstring(returnStr, "&uuml;", "ь");
		returnStr = strChange.changeSubstring(returnStr, "&#39;", "'");
		returnStr = strChange.changeSubstring(returnStr, "&#63;", "?");
		returnStr = strChange.changeSubstring(returnStr, "&Agrave;", "А");
		returnStr = strChange.changeSubstring(returnStr, "&Aacute;", "Б");
		returnStr = strChange.changeSubstring(returnStr, "&Acirc;", "В");
		returnStr = strChange.changeSubstring(returnStr, "&Atilde;", "Г");
		returnStr = strChange.changeSubstring(returnStr, "&Auml;", "Д");
		returnStr = strChange.changeSubstring(returnStr, "&Egrave;", "И");
		returnStr = strChange.changeSubstring(returnStr, "&Eacute;", "Й");
		returnStr = strChange.changeSubstring(returnStr, "&Ecirc;", "К");
		returnStr = strChange.changeSubstring(returnStr, "&Euml;", "Л");
		returnStr = strChange.changeSubstring(returnStr, "&Igrave;", "М");
		returnStr = strChange.changeSubstring(returnStr, "&Iacute;", "Н");
		returnStr = strChange.changeSubstring(returnStr, "&Icirc;", "О");
		returnStr = strChange.changeSubstring(returnStr, "&Iuml;", "П");
		returnStr = strChange.changeSubstring(returnStr, "&Ograve;", "Т");
		returnStr = strChange.changeSubstring(returnStr, "&Oacute;", "У");
		returnStr = strChange.changeSubstring(returnStr, "&Ocirc;", "Ф");
		returnStr = strChange.changeSubstring(returnStr, "&Otilde;", "Х");
		returnStr = strChange.changeSubstring(returnStr, "&Ouml;", "Ц");
		returnStr = strChange.changeSubstring(returnStr, "&Ugrave;", "Щ");
		returnStr = strChange.changeSubstring(returnStr, "&Uacute;", "Ъ");
		returnStr = strChange.changeSubstring(returnStr, "&Ucirc;", "Ы");
		returnStr = strChange.changeSubstring(returnStr, "&Uuml;", "Ь");
		returnStr = strChange.changeSubstring(returnStr, "&ccedil;", "з");
		returnStr = strChange.changeSubstring(returnStr, "&Ccedil;", "З");
		returnStr = strChange.changeSubstring(returnStr, "&#124;", "|");
		returnStr = strChange.changeSubstring(returnStr, "&#63;", "?");
		returnStr = strChange.changeSubstring(returnStr, "&quot;", "\"");
		returnStr = strChange.changeSubstring(returnStr, "&#39;", "'");
//		returnStr = strChange.changeSubstring(returnStr, "<br>", "\n");
	}

	return returnStr;
}
// Coloca a inicial de uma string em letra maiъscula

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
		
		returnStr = strChange.changeSubstring(returnStr, "а", "a");
		returnStr = strChange.changeSubstring(returnStr, "б", "a");
		returnStr = strChange.changeSubstring(returnStr, "в", "a");
		returnStr = strChange.changeSubstring(returnStr, "г", "a");
		returnStr = strChange.changeSubstring(returnStr, "д", "a");
		returnStr = strChange.changeSubstring(returnStr, "и", "e");
		returnStr = strChange.changeSubstring(returnStr, "й", "e");
		returnStr = strChange.changeSubstring(returnStr, "к", "e");
		returnStr = strChange.changeSubstring(returnStr, "л", "e");
		returnStr = strChange.changeSubstring(returnStr, "м", "i");
		returnStr = strChange.changeSubstring(returnStr, "н", "i");
		returnStr = strChange.changeSubstring(returnStr, "о", "i");
		returnStr = strChange.changeSubstring(returnStr, "п", "i");
		returnStr = strChange.changeSubstring(returnStr, "т", "o");
		returnStr = strChange.changeSubstring(returnStr, "у", "o");
		returnStr = strChange.changeSubstring(returnStr, "ф", "o");
		returnStr = strChange.changeSubstring(returnStr, "х", "o");
		returnStr = strChange.changeSubstring(returnStr, "ц", "o");
		returnStr = strChange.changeSubstring(returnStr, "щ", "u");
		returnStr = strChange.changeSubstring(returnStr, "ъ", "u");
		returnStr = strChange.changeSubstring(returnStr, "ы", "u");
		returnStr = strChange.changeSubstring(returnStr, "ь", "u");
		returnStr = strChange.changeSubstring(returnStr, "А", "A");
		returnStr = strChange.changeSubstring(returnStr, "Б", "A");
		returnStr = strChange.changeSubstring(returnStr, "В", "A");
		returnStr = strChange.changeSubstring(returnStr, "Г", "A");
		returnStr = strChange.changeSubstring(returnStr, "Д", "A");
		returnStr = strChange.changeSubstring(returnStr, "И", "E");
		returnStr = strChange.changeSubstring(returnStr, "Й", "E");
		returnStr = strChange.changeSubstring(returnStr, "К", "E");
		returnStr = strChange.changeSubstring(returnStr, "Л", "E");
		returnStr = strChange.changeSubstring(returnStr, "М", "I");
		returnStr = strChange.changeSubstring(returnStr, "Н", "I");
		returnStr = strChange.changeSubstring(returnStr, "О", "I");
		returnStr = strChange.changeSubstring(returnStr, "П", "I");
		returnStr = strChange.changeSubstring(returnStr, "Т", "O");
		returnStr = strChange.changeSubstring(returnStr, "У", "O");
		returnStr = strChange.changeSubstring(returnStr, "Ф", "O");
		returnStr = strChange.changeSubstring(returnStr, "Х", "O");
		returnStr = strChange.changeSubstring(returnStr, "Ц", "O");
		returnStr = strChange.changeSubstring(returnStr, "Щ", "U");
		returnStr = strChange.changeSubstring(returnStr, "Ъ", "U");
		returnStr = strChange.changeSubstring(returnStr, "Ы", "U");
		returnStr = strChange.changeSubstring(returnStr, "Ь", "U");
		returnStr = strChange.changeSubstring(returnStr, "з", "c");
		returnStr = strChange.changeSubstring(returnStr, "З", "C");
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
		returnStr = strChange.changeSubstring(returnStr, "а", "&agrave;");
		returnStr = strChange.changeSubstring(returnStr, "б", "&aacute;");
		returnStr = strChange.changeSubstring(returnStr, "в", "&acirc;");
		returnStr = strChange.changeSubstring(returnStr, "г", "&atilde;");
		returnStr = strChange.changeSubstring(returnStr, "д", "&auml;");
		returnStr = strChange.changeSubstring(returnStr, "и", "&egrave;");
		returnStr = strChange.changeSubstring(returnStr, "й", "&eacute;");
		returnStr = strChange.changeSubstring(returnStr, "к", "&ecirc;");
		returnStr = strChange.changeSubstring(returnStr, "л", "&euml;");
		returnStr = strChange.changeSubstring(returnStr, "м", "&igrave;");
		returnStr = strChange.changeSubstring(returnStr, "н", "&iacute;");
		returnStr = strChange.changeSubstring(returnStr, "о", "&icirc;");
		returnStr = strChange.changeSubstring(returnStr, "п", "&iuml;");
		returnStr = strChange.changeSubstring(returnStr, "т", "&ograve;");
		returnStr = strChange.changeSubstring(returnStr, "у", "&oacute;");
		returnStr = strChange.changeSubstring(returnStr, "ф", "&ocirc;");
		returnStr = strChange.changeSubstring(returnStr, "х", "&otilde;");
		returnStr = strChange.changeSubstring(returnStr, "ц", "&ouml;");
		returnStr = strChange.changeSubstring(returnStr, "щ", "&ugrave;");
		returnStr = strChange.changeSubstring(returnStr, "ъ", "&uacute;");
		returnStr = strChange.changeSubstring(returnStr, "ы", "&ucirc;");
		returnStr = strChange.changeSubstring(returnStr, "ь", "&uuml;");
		returnStr = strChange.changeSubstring(returnStr, "А", "&Agrave;");
		returnStr = strChange.changeSubstring(returnStr, "Б", "&Aacute;");
		returnStr = strChange.changeSubstring(returnStr, "В", "&Acirc;");
		returnStr = strChange.changeSubstring(returnStr, "Г", "&Atilde;");
		returnStr = strChange.changeSubstring(returnStr, "Д", "&Auml;");
		returnStr = strChange.changeSubstring(returnStr, "И", "&Egrave;");
		returnStr = strChange.changeSubstring(returnStr, "Й", "&Eacute;");
		returnStr = strChange.changeSubstring(returnStr, "К", "&Ecirc;");
		returnStr = strChange.changeSubstring(returnStr, "Л", "&Euml;");
		returnStr = strChange.changeSubstring(returnStr, "М", "&Igrave;");
		returnStr = strChange.changeSubstring(returnStr, "Н", "&Iacute;");
		returnStr = strChange.changeSubstring(returnStr, "О", "&Icirc;");
		returnStr = strChange.changeSubstring(returnStr, "П", "&Iuml;");
		returnStr = strChange.changeSubstring(returnStr, "Т", "&Ograve;");
		returnStr = strChange.changeSubstring(returnStr, "У", "&Oacute;");
		returnStr = strChange.changeSubstring(returnStr, "Ф", "&Ocirc;");
		returnStr = strChange.changeSubstring(returnStr, "Х", "&Otilde;");
		returnStr = strChange.changeSubstring(returnStr, "Ц", "&Ouml;");
		returnStr = strChange.changeSubstring(returnStr, "Щ", "&Ugrave;");
		returnStr = strChange.changeSubstring(returnStr, "Ъ", "&Uacute;");
		returnStr = strChange.changeSubstring(returnStr, "Ы", "&Ucirc;");
		returnStr = strChange.changeSubstring(returnStr, "Ь", "&Uuml;");
		returnStr = strChange.changeSubstring(returnStr, "з", "&ccedil;");
		returnStr = strChange.changeSubstring(returnStr, "З", "&Ccedil;");
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
		returnStr = strChange.changeSubstring(returnStr, "а", "a");
		returnStr = strChange.changeSubstring(returnStr, "&aacute;", "a");
		returnStr = strChange.changeSubstring(returnStr, "б", "a");
		returnStr = strChange.changeSubstring(returnStr, "&acirc;",  "a");
		returnStr = strChange.changeSubstring(returnStr, "в",  "a");
		returnStr = strChange.changeSubstring(returnStr, "&atilde;", "a");
		returnStr = strChange.changeSubstring(returnStr, "г", "a");
		returnStr = strChange.changeSubstring(returnStr, "&auml;", "a");
		returnStr = strChange.changeSubstring(returnStr, "д", "a");
		returnStr = strChange.changeSubstring(returnStr, "&egrave;", "e");
		returnStr = strChange.changeSubstring(returnStr, "и", "e");
		returnStr = strChange.changeSubstring(returnStr, "&eacute;", "e");
		returnStr = strChange.changeSubstring(returnStr, "й", "e");
		returnStr = strChange.changeSubstring(returnStr, "&ecirc;", "e");
		returnStr = strChange.changeSubstring(returnStr, "к", "e");
		returnStr = strChange.changeSubstring(returnStr, "&euml;", "e");
		returnStr = strChange.changeSubstring(returnStr, "л", "e");
		returnStr = strChange.changeSubstring(returnStr, "&igrave;", "i");
		returnStr = strChange.changeSubstring(returnStr, "м", "i");
		returnStr = strChange.changeSubstring(returnStr, "&iacute;", "i");
		returnStr = strChange.changeSubstring(returnStr, "н", "i");
		returnStr = strChange.changeSubstring(returnStr, "&icirc;", "i");
		returnStr = strChange.changeSubstring(returnStr, "о", "i");
		returnStr = strChange.changeSubstring(returnStr, "&iuml;", "i");
		returnStr = strChange.changeSubstring(returnStr, "п", "i");
		returnStr = strChange.changeSubstring(returnStr, "&ograve;", "o");
		returnStr = strChange.changeSubstring(returnStr, "т", "o");
		returnStr = strChange.changeSubstring(returnStr, "&oacute;", "o");
		returnStr = strChange.changeSubstring(returnStr, "у", "o");
		returnStr = strChange.changeSubstring(returnStr, "&ocirc;", "o");
		returnStr = strChange.changeSubstring(returnStr, "ф", "o");
		returnStr = strChange.changeSubstring(returnStr, "&otilde;", "o");
		returnStr = strChange.changeSubstring(returnStr, "х", "o");
		returnStr = strChange.changeSubstring(returnStr, "&ouml;", "o");
		returnStr = strChange.changeSubstring(returnStr, "ц", "o");
		returnStr = strChange.changeSubstring(returnStr, "&ugrave;", "u");
		returnStr = strChange.changeSubstring(returnStr, "щ", "u");
		returnStr = strChange.changeSubstring(returnStr, "&uacute;", "u");
		returnStr = strChange.changeSubstring(returnStr, "ъ", "u");
		returnStr = strChange.changeSubstring(returnStr, "&ucirc;", "u");
		returnStr = strChange.changeSubstring(returnStr, "ы", "u");
		returnStr = strChange.changeSubstring(returnStr, "&uuml;", "u");
		returnStr = strChange.changeSubstring(returnStr, "ь", "u");
		returnStr = strChange.changeSubstring(returnStr, "'", "");
		returnStr = strChange.changeSubstring(returnStr, "?", "");
		returnStr = strChange.changeSubstring(returnStr, "&Agrave;", "A");
		returnStr = strChange.changeSubstring(returnStr, "А", "A");
		returnStr = strChange.changeSubstring(returnStr, "&Aacute;", "A");
		returnStr = strChange.changeSubstring(returnStr, "Б", "A");
		returnStr = strChange.changeSubstring(returnStr, "&Acirc;", "A");
		returnStr = strChange.changeSubstring(returnStr, "В", "A");
		returnStr = strChange.changeSubstring(returnStr, "&Atilde;", "A");
		returnStr = strChange.changeSubstring(returnStr, "Г", "A");
		returnStr = strChange.changeSubstring(returnStr, "&Auml;", "A");
		returnStr = strChange.changeSubstring(returnStr, "Д", "A");
		returnStr = strChange.changeSubstring(returnStr, "&Egrave;", "E");
		returnStr = strChange.changeSubstring(returnStr, "И", "E");
		returnStr = strChange.changeSubstring(returnStr, "&Eacute;", "E");
		returnStr = strChange.changeSubstring(returnStr, "Й", "E");
		returnStr = strChange.changeSubstring(returnStr, "&Ecirc;", "E");
		returnStr = strChange.changeSubstring(returnStr, "К", "E");
		returnStr = strChange.changeSubstring(returnStr, "&Euml;", "E");
		returnStr = strChange.changeSubstring(returnStr, "Л", "E");
		returnStr = strChange.changeSubstring(returnStr, "&Igrave;", "I");
		returnStr = strChange.changeSubstring(returnStr, "М", "I");
		returnStr = strChange.changeSubstring(returnStr, "&Iacute;", "I");
		returnStr = strChange.changeSubstring(returnStr, "Н", "I");
		returnStr = strChange.changeSubstring(returnStr, "&Icirc;", "I");
		returnStr = strChange.changeSubstring(returnStr, "О", "I");
		returnStr = strChange.changeSubstring(returnStr, "&Iuml;", "I");
		returnStr = strChange.changeSubstring(returnStr, "П", "I");
		returnStr = strChange.changeSubstring(returnStr, "&Ograve;", "O");
		returnStr = strChange.changeSubstring(returnStr, "Т", "O");
		returnStr = strChange.changeSubstring(returnStr, "&Oacute;", "O");
		returnStr = strChange.changeSubstring(returnStr, "У", "O");
		returnStr = strChange.changeSubstring(returnStr, "&Ocirc;", "O");
		returnStr = strChange.changeSubstring(returnStr, "Ф", "O");
		returnStr = strChange.changeSubstring(returnStr, "&Otilde;", "O");
		returnStr = strChange.changeSubstring(returnStr, "Х", "O");
		returnStr = strChange.changeSubstring(returnStr, "&Ouml;", "O");
		returnStr = strChange.changeSubstring(returnStr, "Ц", "O");
		returnStr = strChange.changeSubstring(returnStr, "&Ugrave;", "U");
		returnStr = strChange.changeSubstring(returnStr, "Щ", "U");
		returnStr = strChange.changeSubstring(returnStr, "&Uacute;", "U");
		returnStr = strChange.changeSubstring(returnStr, "Ъ", "U");
		returnStr = strChange.changeSubstring(returnStr, "&Ucirc;", "U");
		returnStr = strChange.changeSubstring(returnStr, "Ы", "U");
		returnStr = strChange.changeSubstring(returnStr, "&Uuml;", "U");
		returnStr = strChange.changeSubstring(returnStr, "Ь", "U");
		returnStr = strChange.changeSubstring(returnStr, "&ccedil;", "c");
		returnStr = strChange.changeSubstring(returnStr, "з", "c");
		returnStr = strChange.changeSubstring(returnStr, "&Ccedil;", "C");
		returnStr = strChange.changeSubstring(returnStr, "З", "C");
		returnStr = strChange.changeSubstring(returnStr, "&#124;", "|");
		returnStr = strChange.changeSubstring(returnStr, "&#63;", "?");
		returnStr = strChange.changeSubstring(returnStr, "&quot;","\"");
		returnStr = strChange.changeSubstring(returnStr, "&#39;","'");
		returnStr = strChange.changeSubstring(returnStr, "<br>","\n");
	}

	return returnStr;
}
}
