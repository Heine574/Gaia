def RPGgame(user, char, location):
    f = open('data/charlocations.txt')
    mylocs = f.read().split('\n')
    f.close()
    myloc = {}
    for i in mylocs:
        t = i.split(': ')
        if len(t) > 1:
            myloc[t[0]] = t[1]
    if not user in myloc:
        myloc[char] = location
    f = open('data/charlocations.txt', 'w')
    for i in myloc:
        f.write(i + ': ' + myloc[i] + '\n')
    f.close()
    ret = '<form action="register.php" method="post" enctype="text/plain" onsubmit="AJAXSubmit(this); return false;"><fieldset>'
    ret += '<p>Logged in as <input type="text" name="user" disabled value="'
    ret += user
    ret += '" /><p>Selected character <input type="text" name="playcharacter" disabled value="'
    ret += char
    ret += '" /><p>Selected location <input type="text" name="location" disabled value="'
    ret += location
    ret += '" /><p>Your message:<br /><textarea name="message" cols="40" rows="8"></textarea></p><p><input type="submit" value="Submit" /></p></fieldset></form>'
    return ret
def charselect(user):
    f = open('data/users.txt')
    data = f.read().split('\n')
    f.close()
    f = open('data/characters.txt')
    chars = f.read().split('\n')
    f.close()
    chars = chars[data.index(user)].split(', ')
    f = open('data/locations.txt')
    locs = f.read().split('\n')
    f.close()
    ret = '<form action="register.php" method="post" enctype="text/plain" onsubmit="AJAXSubmit(this); return false;"><fieldset>'
    ret += '<p>Logged in as <input type="text" name="user" disabled value="'
    ret += user
    ret += '" /><p>Character: <select name="selcharacter">'
    for i in chars:
        ret += '<option value="' + i + '">' + i + '</option>'
    ret += '</select></p><p>Location: <select name="location">'
    for i in locs:
        ret += '<option value="' + i.split(': ')[0] + '">' + i.split(': ')[0] + '</option>'
    ret += '</select></p><p><input type="submit" value="Submit" /></p></fieldset></form>'
    return ret
def createchar(user):
    ret = '<form action="register.php" method="post" enctype="text/plain" onsubmit="AJAXSubmit(this); return false;"><fieldset>'
    ret += '<p>Logged in as <input type="text" name="user" disabled value="'
    ret += user
    ret += '" /></p><p>New character name: <input type="text" name="newcharname" /></p>'
    ret += '<p><input class="button" type="submit" value="Submit" /></p>'
    return ret
pages = {'RPGgame':RPGgame, 'createchar':createchar, 'charselect':charselect}
