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

class StringChanger {
	private String baseString;
	private int currentPosition;
/**
 * This method was created in VisualAge.
 */
public StringChanger() {
	super();
}
/**
 * StringChanger constructor comment.
 */
public StringChanger(String aString) {
	super();

	this.baseString = aString;
}
/**
 * changeString method
 *
 * changes the occurencies of oldString by newString in the baseString
 *
 * @return java.lang.String
 * @param oldString java.lang.String	the substring to be changed
 * @param newString java.lang.String	the new substring to insert
 */
public String changeSubstring(String oldString, String newString) throws Exception {
	this.currentPosition = 0;

	while (hasMoreOccurrences(oldString))
	{
		String auxString = baseString.substring(0, currentPosition);
		auxString = auxString + newString;
		auxString = auxString + baseString.substring(currentPosition + oldString.length());

		currentPosition = currentPosition + newString.length();
		baseString = auxString;
	}
	
	return baseString;
}
/**
 * changeString method
 *
 * changes the occurencies of oldString by newString in aString
 *
 * @return java.lang.String
 * @param aString java.lang.String		the string to make the change
 * @param oldString java.lang.String	the substring to change
 * @param newString java.lang.String	the new substring to insert
 */
public String changeSubstring(String aString, String oldString, String newString) throws Exception {
	this.baseString = aString;

	return changeSubstring(oldString, newString);
}
/**
 * hasMoreOccurencies method
 *
 * checks if there are more occurencies of searchStr in baseString
 *
 * @return boolean
 * @param searchStr java.lang.String	the substring to be searched
 */
private boolean hasMoreOccurrences(String searchStr) throws Exception {
	int start = baseString.indexOf(searchStr, currentPosition);

	if (start != -1)
	{
		currentPosition = start;
		return true;
	}
	else
	{
		currentPosition = baseString.length();
		return false;
	}
}
}
