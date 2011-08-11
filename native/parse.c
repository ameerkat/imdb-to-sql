/*
 * This is an attempt to use a native parser instead of a python regex to achieve
 * better performance from the sqlite conversion script
 * Ameer Ayoub <ameer.ayoub@gmail.com>
 */
#include <Python.h>
#include <stdio.h>
#include <string.h>
#include <ctype.h>

#define MAX_NICKNAME_LEN 			256
#define MAX_LASTNAME_LEN 			256
#define MAX_FIRSTNAME_LEN 			256
#define MAX_ACTORNUMBER_LEN 		16
#define MAX_TITLE_LEN				256
#define MAX_YEAR_LEN				5
#define	MAX_CODE_LEN				3
#define MAX_EXTRA_INFO_LEN			128
#define MAX_EPISODE_TITLE_LEN		256
#define MAX_EPISODE_SERIES_LEN		8
#define MAX_EPISODE_NUMBER_LEN		8
#define MAX_CHARACTER_NAME_LEN		256
#define MAX_BILLING_POSITION_LEN	8
#define MAX_NUMBER_LEN				16
//#define LINE_SIZE 				511

#define skip_whitespace(PTR) while(isspace(*PTR)){++PTR;}
#define year_d(POS) (*(POS) == '?' || isdigit(*(POS)))

int 
_parse_actor(
	const char *input,
   	char *nickname,
   	char *lastname,
   	char *firstname,
   	char *actornumber){
	const char *current_pos = input;
	const char *pos; // temp
	int is_nick = 0;
	// initialize all information to empty strings
	*nickname = '\0';
	*lastname = '\0';
	*firstname = '\0';
	*actornumber = '\0';
	if (!*current_pos){
		// error : can not process 0 length string
		return 0;
	}
	// check for nickname
	if (*current_pos == '\''){
		// This may be a nickname or the start of a name
		pos = current_pos+1;
		while(*pos && *(pos+1) && !(*pos == '\'' && *(pos+1) == ' '))
			++pos;
		if (*pos && *(pos+1) && *pos == '\'' && *(pos+1) == ' ') {
			strncpy(nickname, current_pos+1, pos-current_pos-1);
			nickname[pos-current_pos-1] = '\0'; // doesn't get copied I guess
			current_pos = pos+1;
		}
	}
	if (*current_pos && *current_pos != ','){
		// Parse last name
		skip_whitespace(current_pos);
		pos = current_pos;
		while(*pos && *pos != ',' && *pos != '(')
			++pos;
		strncpy(lastname, current_pos, pos - current_pos);
		lastname[pos-current_pos] = '\0'; // doesn't get copied I guess
		current_pos = pos;
	}
	if (*current_pos && *current_pos == ','){
		// Parse first name
		++current_pos;
		skip_whitespace(current_pos);
		pos = current_pos;
		while(*pos && *pos != '(')
			++pos;
		strncpy(firstname, current_pos, pos - current_pos);
		firstname[pos-current_pos] = '\0'; // doesn't get copied I guess
		current_pos = pos;
	}
	if (*current_pos && *current_pos == '('){
		// Parse actor number
		++current_pos;
		pos = current_pos;
		while(*pos && *pos != ')')
			++pos;
		strncpy(actornumber, current_pos, pos - current_pos);
		actornumber[pos-current_pos] = '\0'; // doesn't get copied I guess
		current_pos = pos;
	}
	if(!*nickname && !*firstname && !*actornumber){
		// If we only read in one name then set it to firstname instead of lastname
		strcpy(firstname, lastname);
		*lastname = '\0';
	}
	return 1;
}

int 
_parse_acted_in(
	const char* input,
   	char* title, 
	char* year, 
	char *number,
	char* code, 
	char* extra_info, 
	char* episode_title,
	char* episode_series, 
	char* episode_number, 
	char* character_name, 
	char* billing_position){

	const char *current_pos = input;
	const char *pos; // temp
	*title = '\0';
	*year = '\0';
	*number = '\0';
	*code = '\0';
	*extra_info = '\0';
	*episode_title = '\0';
	*episode_series = '\0';
	*episode_number = '\0';
	*character_name = '\0';
	*billing_position = '\0';
	if (!*current_pos){
		// error : can not process 0 length string
		return 0;
	}
	if (*current_pos == '\"'){
		// TV series style title
		pos = current_pos+1;
		while(*pos && *(pos+1) && !(*pos == '\"' && *(pos+1) == ' '))
			++pos;
		strncpy(title, current_pos+1, pos-current_pos-1);
		title[pos-current_pos-1] = '\0';
		current_pos = pos+1;
	} else {
		pos = current_pos;
		// We have to differentiate between parenthesized title text and the year, the year
		// should consist of digits or question marks
		while(*pos && *(pos+1) && *(pos+2) && *(pos+3) && *(pos+4) && *(pos+5) &&
			!(*pos == '(' && year_d(pos+1) && year_d(pos+2)
			&& year_d(pos+3) && year_d(pos+4) && (*(pos+5) == ')' || *(pos+5) == '/')))
			++pos;
		strncpy(title, current_pos, pos-current_pos);
		title[pos-current_pos] = '\0';
		current_pos = pos-1;
	}
	skip_whitespace(current_pos); // in case quoted
	strncpy(year, current_pos+1, 4);
	year[4] = '\0';
	current_pos += 5;
	if(*current_pos == '/'){
		++current_pos;
		pos = current_pos;
		while(*pos && *pos != ')')
			++pos;
		strncpy(number, current_pos, pos-current_pos);
		number[pos-current_pos] = '\0';
	} else {
		++current_pos; // skip teh trailing )
	}
	skip_whitespace(current_pos);
	if (*current_pos && *current_pos == '('){
		if((*(current_pos+1) == 'V') || (*(current_pos+1) == 'T' && *(current_pos+2) == 'V') ||
				(*(current_pos+1) == 'V' && *(current_pos+2) == 'G')){
			// Parse out special code
			++current_pos;
			pos = current_pos;
			while(*pos && *pos != ')' && *pos != '/')
				++pos;
			strncpy(code, current_pos, pos-current_pos);
			code[pos-current_pos] = '\0';
			current_pos = pos+1;
			skip_whitespace(current_pos);
		}
	}
	if (*current_pos && *current_pos == '{'){
		// Parse out episode information
		pos = current_pos+1;
		while(*pos && *pos != '(' && *pos != '}')
			++pos;
		strncpy(episode_title, current_pos+1, pos-current_pos-1);
		episode_title[pos-current_pos-1] = '\0';
		if (*pos == '(' && *(pos+1) == '#'){
			current_pos = pos+2; // skip over '(' and '#'
			pos = current_pos;
			while(*pos && *pos != '.')
				++pos;
			strncpy(episode_series, current_pos, pos-current_pos);
			episode_series[pos-current_pos] = '\0';
			current_pos = pos+1;
			pos = current_pos;
			while(*pos && *pos != ')')
				++pos;
			strncpy(episode_number, current_pos, pos-current_pos);
			episode_number[pos-current_pos] = '\0';
			current_pos = pos+2;
		} else if (*pos == '('){
			// We could just seperate this out perhaps into a episode date later
			++pos;
			while(*pos && *pos != ')')
				++pos;
			strncpy(episode_title, current_pos+2, pos-current_pos-2);
			episode_title[pos-current_pos-2] = '\0';
			current_pos = pos;
		}
		skip_whitespace(current_pos);
	}
	if (*current_pos && *current_pos == '('){
		// Parse out extra information
		++current_pos;
		pos = current_pos;
		while(*pos && *pos != ')')
			++pos;
		strncpy(extra_info, current_pos, pos-current_pos);
		extra_info[pos-current_pos] = '\0';
		current_pos = pos+1;
		skip_whitespace(current_pos);
	}
	if (*current_pos && *current_pos == '['){
		// Parse out character information
		pos = ++current_pos;
		while(*pos && *pos != ']')
			++pos;
		strncpy(character_name, current_pos, pos-current_pos);
		character_name[pos-current_pos] = '\0';
		current_pos = pos+1;
		skip_whitespace(current_pos);
	}
	if (*current_pos && *current_pos == '<'){
		// Parse out billing position
		pos = ++current_pos;
		while(*pos && *pos != '>')
			++pos;
		strncpy(billing_position, current_pos, pos-current_pos);
		billing_position[pos-current_pos] = '\0';
		current_pos = pos+1;
	}
	return 1;
}

static PyObject *
parse_actor(PyObject *self, PyObject *args){
	const char* input;
	char nickname[MAX_NICKNAME_LEN];
	char lastname[MAX_LASTNAME_LEN];
	char firstname[MAX_FIRSTNAME_LEN];
	char actornumber[MAX_ACTORNUMBER_LEN]; // This is a roman numeral
	
	if(!PyArg_ParseTuple(args, "s", &input))
		return Py_None;
	if(_parse_actor(input, nickname, lastname, firstname, actornumber))
		return Py_BuildValue("(s, s, s, s)", 
			nickname, lastname, firstname, actornumber);
	else
		return Py_None;
}

static PyObject *
parse_acted_in(PyObject *self, PyObject *args){
	const char* input;
	char title[MAX_TITLE_LEN];
	char year[MAX_YEAR_LEN];
	char number[MAX_NUMBER_LEN];
	char code[MAX_CODE_LEN];
	char extra_info[MAX_EXTRA_INFO_LEN];
	char episode_title[MAX_EPISODE_TITLE_LEN];
	char episode_series[MAX_EPISODE_SERIES_LEN];
	char episode_number[MAX_EPISODE_NUMBER_LEN];
	char character_name[MAX_CHARACTER_NAME_LEN];
	char billing_position[MAX_BILLING_POSITION_LEN];
	
	if(!PyArg_ParseTuple(args, "s", &input))
		return Py_None;
	if(_parse_acted_in(input, title, year, number, code, extra_info, episode_title, episode_series,
		episode_number, character_name, billing_position))
		return Py_BuildValue("(s, s, s, s, s, s, s, s, s, s)", 
			title, year, number, code, extra_info, episode_title, episode_series, episode_number, 
			character_name, billing_position);
	else
		return Py_None;
}

/*
int t_getline(char *line, size_t maxsize){
	int c, i = 0;
	while((c = getchar()) != EOF && c != '\n' && ++i < maxsize){
		*(line++) = c;
	}
	*line = '\0';
	return i;
}
*/

static PyMethodDef ParseMethods[] = {
	{"actor", parse_actor, METH_VARARGS, "Parses out actor information from a string."},
	{"acted_in", parse_acted_in, METH_VARARGS, "Parses out acted in information from a string."},
	{NULL, NULL, 0, NULL}
};

PyMODINIT_FUNC
initparse(void){
	(void) Py_InitModule("parse", ParseMethods);
}

/*
int main(void){
	int c;
	char line[LINE_SIZE];
	char nickname[MAX_NICKNAME_LEN];
	char lastname[MAX_LASTNAME_LEN];
	char firstname[MAX_FIRSTNAME_LEN];
	char actornumber[MAX_ACTORNUMBER_LEN]; // This is a roman numeral
	while(t_getline(line, sizeof(line))){
		parse_as(line, nickname, lastname, firstname, actornumber);
		printf("input: %s\noutput:\n\tnickname: \t%s\n\tlastname: \t%s\n\tfirstname: \t%s\n\tactornumber: \t%s\n",
		   line, nickname, lastname, firstname, actornumber);
	}
	return 0;
}
*/

