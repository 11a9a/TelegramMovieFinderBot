import random, requests as rqst

# class test_bot:
#paste ur token here
urToken = '<urToken>/'

url = 'https://api.telegram.org/bot' + urToken

def get_update(url):
	response = rqst.get(url + "getUpdates") #returns <class 'requests.models.Response'> , value <Response [200]>
	response = response.json() #returns <class 'dict'> inside JSON file
	result = response['result'] #returns <class 'list'> inside List choosen from JSON file
	index_last_update = len(result) - 1
	return result[index_last_update]

def get_chat_id(update):
	chat_id = get_update(url)['message']['chat']['id']
	return chat_id

def get_message_text(update):
	message_text = get_update(url)['message']['text']
	return message_text

def get_username(update):
	username = get_update(url)['message']['from']['first_name'] + " " + get_update(url)['message']['from']['last_name']
	return username

def send_message(chat_id, message_text):
	params = {"chat_id": chat_id, "text": message_text}
	response = rqst.post(url + 'sendMessage', data = params)
	return response

def send_photo(chat_id , photo, caption):
	params = {"chat_id": chat_id, "photo": photo, "caption": caption}
	response = rqst.post(url + 'sendPhoto', data = params)
	return response

def get_movie(movie_title):
	#add ur apikey here
	urApiKey = '<urApiKey>'
	response = rqst.get('http://www.omdbapi.com/?{}}&t={}'.format(urApiKey, movie_title))
	response = response.json()
	return response

def is_movie_command(message_text):
	return message_text[7:] if message_text[0:7] == '/movie ' else ""

def is_book_command(message_text):
	return message_text[6:] if message_text[0:6] == '/book ' else ""

def main():
	update_id = get_update(url)['update_id']
	while True:
		update = get_update(url)
		if update_id == update['update_id']:
			movie_name = is_movie_command(get_message_text(update))
			if movie_name:
				movie = get_movie(movie_name)
				caption = 'Title: ' + movie['Title'] + '\nYear: ' + movie['Year'] + '\nRuntime: ' + movie['Runtime']
				send_photo(get_chat_id(update), movie['Poster'], caption)
	
			update_id += 1

main()