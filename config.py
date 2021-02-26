# Token from @botfather #
API_TOKEN = "1234:abcd"

# Data from the database #
DATADB = {
	"user": "", 
	"host": "", 
	"database": "", 
	"password": "", 
	"port": 5432
}

# ---------Settings--------- #

# Logging type #
LOGGING_TYPE="console" # "console" or "file" 

# ---------Settings--------- #

# List of symbols allowed for prefix #
slist = "/!?.,*%:'\"+=)(@-_&₽#$€¥¢©®™~¿¡^><}{][`;÷|¦¬×§¶°\\"

class times:
	day = ["day", "days", "d", "день", "дней", "день", "д", "сутки", "суток", "с"]
	min = ["min", "minute", "minutes", "m", "минут", "минута", "минуты", "мин", "м"]
	hr = ["hr", "hour", "hours", "h", "час", "часа", "часов", "ч"]
	week = ["week", "weeks", "w", "неделя", "недели", "недель", "н"]
	month = ["month", "months", "M", "месяц", "месяца", "месяца", "М"]
	year = ["year", "years", "y", "год", "года", "г", "лет", "л"]


# Text for commands #
class stng:
	stngs = """Доступные для изменения настройки:
  1. serror [true|false] - если произошла какая-либо ошибка, то бот не будет об этом сообщать ({0})
  2. autoReplace [true|false] - если человек написал неправильно какую-либо команду, то бот это поймёт и всё равно ответ на эту команду ({2})
  3. prefix [symbol] ({1}prefix) - префикс сообщения ({1})
  4. welcome [text] ({1}welcome) - приветствие при приглашении ({3})
  5. offcommand [command_name] ({1}offcmd) - отключение команд ({4} из {5} включено)
Введите {1}settings [value] [setting] чтобы изменить настройку."""

	stngsbool = ["serror", "autoreplace"]
	stngstr = ["prefix", "welcome", "offcommand"]
	cmds = ["id", "prefix", "kick", "stats", "welcome", "ban", "unban", "banlist", "top", "chatstats", "setrang"]
	
# Chat rangs #
class rangs:
	USER = 1
	ADMIN = 2
	CREATOR = 3

# Для команды setrang #
admin = ["admin", "administrator", "adm", "админ", "администратор", "адм"]
user = ["user", "usr", "юзер", "юзр", "пользователь"]

# All cmds #
cmds = ["id", "prefix", "kick", "unban", "ban", "banlist", "stats", "settings", "offcmd", "welcome", "top", "chatstats", "setrang"]

# Commands in class (The first argument should be right) #
class commands:
	id = ["id", "ид", "айди"]
	prefix = ["prefix", "symbol", "префикс", "символ"]
	start = ["start", "starts", "старт", "стартс", "начать", "начало"]
	kick = ["kick", "исключить", "выкинуть", "кикнуть", "кик"]
	ban = ["ban", "banhammer", "забанить", "бан", "банхаммер"]
	banlist = ["banlist", "listban", "bans", "banslist", "listbans", "банлист", "листбан", "бансписок", "списокбанов", "банс"]
	unban = ["unban", "pardon", "разбанить", "разблокировать", "анбан", "разбан"]
	unkick = ["unkick", "раскикнуть", "анкик"]
	setrang = ["setrang", "setrank", "setstatus",  "status", "сетранг", "сетранк", "сетстатус", "статус"]
	top = ["top", "tops", "bests", "best", "топ", "топы", "лучшие", "лучший"]
	stats = ["stats", "statistic", "stat", "statistica", "стат", "стата", "статистика", "статистик", "статс"]
	chatstats = ["chatstats", "chatstatistic", "chatstat", "chatstatistica", "chatstats", "чатстат", "чатстата", "чатстатистика", "чатстатистик", "чатстатс"]
	settings = ["settings", "setings", "setting", "seting", "stngs", "настройки", "настройка", "сетингс", "сеттингс"]
	offcmd = ["offcmd", "offcmds", "offcommand", "offcommands", "команда", "команды", "выклкоманду", "вклкоманду", "оффкмд"]
	welcome = ["welcome", "greet", "приветствие", "здравствуйте", "велком"] 