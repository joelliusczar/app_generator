from datetime import datetime
from typing import List, Any
from <%= projectNameSnake %>.dtos_and_utilities import (
	AccountInfo,
	UserRoleDef,
	RulePriorityLevel,
	MinItemSecurityLevel
)
try:
	from .special_strings_reference import chinese1, irish1
except:
	#for if I try to import file from interactive
	from special_strings_reference import chinese1, irish1


bravo_user_id = 2
charlie_user_id = 3
delta_user_id = 4
echo_user_id = 5 #can't use. No password
foxtrot_user_id = 6
golf_user_id = 7
hotel_user_id = 8
india_user_id = 9
juliet_user_id = 10
kilo_user_id = 11
lima_user_id = 12
mike_user_id = 13
november_user_id = 14
oscar_user_id = 15
papa_user_id = 16
quebec_user_id = 17
romeo_user_id = 18 #designated no roles user
sierra_user_id = 19
tango_user_id = 20
uniform_user_id = 21
victor_user_id = 22
whiskey_user_id = 23
xray_user_id = 24
yankee_user_id = 25
zulu_user_id = 26
alice_user_id = 27
bertrand_user_id = 28
carl_user_id = 29
dan_user_id = 30
felix_user_id = 31
foxman_user_id = 32
foxtrain_user_id = 33
george_user_id = 34
hamburger_user_id = 35
horsetel_user_id = 36
ingo_user_id = 37
ned_land_user_id = 38
narlon_user_id = 39
number_user_id = 40
oomdwell_user_id = 41
paul_bear_user_id = 42
quirky_admin_user_id = 43
radical_path_user_id = 44
station_saver_user_id = 45
super_path_user_id = 46
tossed_slash_user_id = 47
unruled_station_user_id = 48



def get_user_params(
	orderedTestDates: List[datetime],
	primaryUser: AccountInfo,
	testPassword: bytes
) -> list[dict[Any, Any]]:
	global users_params
	users_params = [
		{
			"pk": primaryUser.id,
			"username": primaryUser.username,
			"displayname": None,
			"hashedpw": testPassword,
			"email": primaryUser.email,
			"isdisabled": False,
			"creationtimestamp": orderedTestDates[0].timestamp(),
			"dirroot": ""
		},
		{
			"pk": bravo_user_id,
			"username": "testUser_bravo",
			"displayname": "Bravo Test User",
			"hashedpw": testPassword,
			"email": "test2@test.com",
			"isdisabled": False,
			"creationtimestamp": orderedTestDates[1].timestamp(),
			"dirroot": None
		},
		{
			"pk": charlie_user_id,
			"username": "testUser_charlie",
			"displayname": "charlie the user of tests",
			"hashedpw": None,
			"email": "test3@test.com",
			"isdisabled": False,
			"creationtimestamp": orderedTestDates[1].timestamp(),
			"dirroot": None
		},
		{
			"pk": delta_user_id,
			"username": "testUser_delta",
			"displayname": "DELTA USER",
			"hashedpw": testPassword,
			"email": "test4@test.com",
			"isdisabled": True,
			"creationtimestamp": orderedTestDates[1].timestamp(),
			"dirroot": None
		},
		{
			"pk": echo_user_id, #can't use. No password
			"username": "testUser_echo",
			"displayname": "ECHO, ECHO",
			"hashedpw": None,
			"email": "test5@test.com",
			"isdisabled": False,
			"creationtimestamp": orderedTestDates[1].timestamp(),
			"dirroot": None
		},
		{
			"pk": foxtrot_user_id,
			"username": "testUser_foxtrot",
			"displayname": "\uFB00 ozotroz",
			"hashedpw": testPassword,
			"email": "test6@test.com",
			"isdisabled": False,
			"creationtimestamp": orderedTestDates[1].timestamp(),
			"dirroot": None
		},
		{
			"pk": golf_user_id,
			"username": "testUser_golf",
			"displayname": None,
			"hashedpw": testPassword,
			"email": "test7@test.com",
			"isdisabled": False,
			"creationtimestamp": orderedTestDates[1].timestamp(),
			"dirroot": None
		},
		{
			"pk": hotel_user_id,
			"username": "testUser_hotel",
			"displayname": None,
			"hashedpw": testPassword,
			"email": "test8@test.com",
			"isdisabled": False,
			"creationtimestamp": orderedTestDates[1].timestamp(),
			"dirroot": None
		},
		{
			"pk": india_user_id,
			"username": "testUser_india",
			"displayname": "IndiaDisplay",
			"hashedpw": testPassword,
			"email": "test9@test.com",
			"isdisabled": False,
			"creationtimestamp": orderedTestDates[1].timestamp(),
			"dirroot": None
		},
		{
			"pk": juliet_user_id,
			"username": "testUser_juliet",
			"displayname": "julietDisplay",
			"hashedpw": testPassword,
			"email": "test10@test.com",
			"isdisabled": False,
			"creationtimestamp": orderedTestDates[1].timestamp(),
			"dirroot": None
		},
		{
			"pk": kilo_user_id,
			"username": "testUser_kilo",
			"displayname": None,
			"hashedpw": testPassword,
			"email": "test11@test.com",
			"isdisabled": False,
			"creationtimestamp": orderedTestDates[1].timestamp(),
			"dirroot": "/foo"
		},
		{
			"pk": lima_user_id,
			"username": "testUser_lima",
			"displayname": None,
			"hashedpw": testPassword,
			"email": "test12@test.com",
			"isdisabled": False,
			"creationtimestamp": orderedTestDates[1].timestamp(),
			"dirroot": None
		},
		{
			"pk": mike_user_id,
			"username": "testUser_mike",
			"displayname": None,
			"hashedpw": testPassword,
			"email": "test13@test.com",
			"isdisabled": False,
			"creationtimestamp": orderedTestDates[1].timestamp(),
			"dirroot": None
		},
		{
			"pk": november_user_id,
			"username": "testUser_november",
			"displayname": "\u006E\u0303ovoper",
			"hashedpw": testPassword,
			"email": "test14@test.com",
			"isdisabled": False,
			"creationtimestamp": orderedTestDates[1].timestamp(),
			"dirroot": None
		},
		{
			"pk": oscar_user_id,
			"username": "testUser_oscar",
			"displayname": None,
			"hashedpw": testPassword,
			"email": "test15@test.com",
			"isdisabled": False,
			"creationtimestamp": orderedTestDates[1].timestamp(),
			"dirroot": None
		},
		{
			"pk": papa_user_id,
			"username": "testUser_papa",
			"displayname": None,
			"hashedpw": testPassword,
			"email": "test16@test.com",
			"isdisabled": False,
			"creationtimestamp": orderedTestDates[1].timestamp(),
			"dirroot": None
		},
		{
			"pk": quebec_user_id,
			"username": "testUser_quebec",
			"displayname": None,
			"hashedpw": testPassword,
			"email": "test17@test.com",
			"isdisabled": False,
			"creationtimestamp": orderedTestDates[1].timestamp(),
			"dirroot": None
		},
		{
			"pk": romeo_user_id,
			"username": "testUser_romeo",
			"displayname": None,
			"hashedpw": testPassword,
			"email": "test18@test.com",
			"isdisabled": False,
			"creationtimestamp": orderedTestDates[1].timestamp(),
			"dirroot": None
		},
		{
			"pk": sierra_user_id,
			"username": "testUser_sierra",
			"displayname": None,
			"hashedpw": testPassword,
			"email": "test19@test.com",
			"isdisabled": False,
			"creationtimestamp": orderedTestDates[1].timestamp(),
			"dirroot": None
		},
		{
			"pk": tango_user_id,
			"username": "testUser_tango",
			"displayname": None,
			"hashedpw": testPassword,
			"email": "test20@test.com",
			"isdisabled": False,
			"creationtimestamp": orderedTestDates[1].timestamp(),
			"dirroot": None
		},
		{
			"pk": uniform_user_id,
			"username": "testUser_uniform",
			"displayname": None,
			"hashedpw": testPassword,
			"email": "test21@test.com",
			"isdisabled": False,
			"creationtimestamp": orderedTestDates[1].timestamp(),
			"dirroot": None
		},
		{
			"pk": victor_user_id,
			"username": "testUser_victor",
			"displayname": None,
			"hashedpw": testPassword,
			"email": "test22@test.com",
			"isdisabled": False,
			"creationtimestamp": orderedTestDates[1].timestamp(),
			"dirroot": None
		},
		{
			"pk": whiskey_user_id,
			"username": "testUser_whiskey",
			"displayname": None,
			"hashedpw": testPassword,
			"email": "test23@test.com",
			"isdisabled": False,
			"creationtimestamp": orderedTestDates[1].timestamp(),
			"dirroot": None
		},
		{
			"pk": xray_user_id,
			"username": "testUser_xray",
			"displayname": None,
			"hashedpw": testPassword,
			"email": "test24@test.com",
			"isdisabled": False,
			"creationtimestamp": orderedTestDates[1].timestamp(),
			"dirroot": None
		},
		{
			"pk": yankee_user_id,
			"username": "testUser_yankee",
			"displayname": None,
			"hashedpw": testPassword,
			"email": "test25@test.com",
			"isdisabled": False,
			"creationtimestamp": orderedTestDates[1].timestamp(),
			"dirroot": None
		},
		{
			"pk": zulu_user_id,
			"username": "testUser_zulu",
			"displayname": None,
			"hashedpw": testPassword,
			"email": "test26@test.com",
			"isdisabled": False,
			"creationtimestamp": orderedTestDates[1].timestamp(),
			"dirroot": None
		},
		{
			"pk": alice_user_id,
			"username": "testUser_alice",
			"displayname": "Alice is my name",
			"hashedpw": testPassword,
			"email": "test27@test.com",
			"isdisabled": False,
			"creationtimestamp": orderedTestDates[1].timestamp(),
			"dirroot": None
		},
		{
			"pk": bertrand_user_id,
			"username": "bertrand",
			"displayname": "Bertrance",
			"hashedpw": testPassword,
			"email": "test28@test.com",
			"isdisabled": False,
			"creationtimestamp": orderedTestDates[1].timestamp(),
			"dirroot": None
		},
		{
			"pk": carl_user_id,
			"username": "carl",
			"displayname": "Carl the Cactus",
			"hashedpw": testPassword,
			"email": "test29@test.com",
			"isdisabled": False,
			"creationtimestamp": orderedTestDates[1].timestamp(),
			"dirroot": None
		},
		{
			"pk": dan_user_id,
			"username": "dan",
			"displayname": "Dookie Dan",
			"hashedpw": testPassword,
			"email": "test30@test.com",
			"isdisabled": False,
			"creationtimestamp": orderedTestDates[1].timestamp(),
			"dirroot": None
		},
		{
			"pk": felix_user_id,
			"username": "felix",
			"displayname": "Felix the man",
			"hashedpw": testPassword,
			"email": "test31@test.com",
			"isdisabled": False,
			"creationtimestamp": orderedTestDates[1].timestamp(),
			"dirroot": None
		},
		{
			"pk": foxman_user_id,
			"username": "foxman",
			"displayname": None,
			"hashedpw": testPassword,
			"email": "test32@test.com",
			"isdisabled": False,
			"creationtimestamp": orderedTestDates[1].timestamp(),
			"dirroot": None
		},
		{
			"pk": foxtrain_user_id,
			"username": "foxtrain",
			"displayname": "Foxtrain chu",
			"hashedpw": testPassword,
			"email": "test33@test.com",
			"isdisabled": False,
			"creationtimestamp": orderedTestDates[1].timestamp(),
			"dirroot": None
		},
		{
			"pk": george_user_id,
			"username": "george",
			"displayname": "George Costanza",
			"hashedpw": testPassword,
			"email": "test35@test.com",
			"isdisabled": False,
			"creationtimestamp": orderedTestDates[1].timestamp(),
			"dirroot": None
		},
		{
			"pk": hamburger_user_id,
			"username": "hamburger",
			"displayname": "HamBurger",
			"hashedpw": testPassword,
			"email": "test36@test.com",
			"isdisabled": False,
			"creationtimestamp": orderedTestDates[1].timestamp(),
			"dirroot": None
		},
		{
			"pk": horsetel_user_id,
			"username": "horsetel",
			"displayname": "horsetelophone",
			"hashedpw": testPassword,
			"email": "test37@test.com",
			"isdisabled": False,
			"creationtimestamp": orderedTestDates[1].timestamp(),
			"dirroot": None
		},
		{
			"pk": ingo_user_id,
			"username": "ingo",
			"displayname": "Ingo      is a bad man",
			"hashedpw": testPassword,
			"email": "test38@test.com",
			"isdisabled": False,
			"creationtimestamp": orderedTestDates[1].timestamp(),
			"dirroot": None
		},
		{
			"pk": ned_land_user_id,
			"username": "ned_land",
			"displayname": "Ned Land of the Spear",
			"hashedpw": testPassword,
			"email": "test39@test.com",
			"isdisabled": False,
			"creationtimestamp": orderedTestDates[1].timestamp(),
			"dirroot": None
		},
		{
			"pk": narlon_user_id,
			"username": "narlon",
			"displayname": "Narloni",
			"hashedpw": testPassword,
			"email": "test40@test.com",
			"isdisabled": False,
			"creationtimestamp": orderedTestDates[1].timestamp(),
			"dirroot": None
		},
		{
			"pk": number_user_id,
			"username": "7",
			"displayname": "seven",
			"hashedpw": testPassword,
			"email": "test41@test.com",
			"isdisabled": False,
			"creationtimestamp": orderedTestDates[1].timestamp(),
			"dirroot": None
		},
		{
			"pk": oomdwell_user_id,
			"username": "testUser_oomdwell",
			"displayname": "Oomdwellmit",
			"hashedpw": testPassword,
			"email": "test42@test.com",
			"isdisabled": False,
			"creationtimestamp": orderedTestDates[1].timestamp(),
			"dirroot": None
		},
		{
			"pk": paul_bear_user_id,
			"username": "paulBear_testUser",
			"displayname": "Paul Bear",
			"hashedpw": testPassword,
			"email": "test43@test.com",
			"isdisabled": False,
			"creationtimestamp": orderedTestDates[1].timestamp(),
			"dirroot": "paulBear_testUser"
		},
		{
			"pk": quirky_admin_user_id,
			"username": "quirkyAdmon_testUser",
			"displayname": "Quirky Admin",
			"hashedpw": testPassword,
			"email": "test44@test.com",
			"isdisabled": False,
			"creationtimestamp": orderedTestDates[1].timestamp(),
			"dirroot": "quirkyAdmon_testUser"
		},
		{
			"pk": radical_path_user_id,
			"username": "radicalPath_testUser",
			"displayname": "Radical Path",
			"hashedpw": testPassword,
			"email": "test45@test.com",
			"isdisabled": False,
			"creationtimestamp": orderedTestDates[1].timestamp(),
			"dirroot": "radicalPath_testUser"
		},
		{
			"pk": station_saver_user_id,
			"username": "stationSaver_testUser",
			"displayname": "Station Saver",
			"hashedpw": testPassword,
			"email": "test46@test.com",
			"isdisabled": False,
			"creationtimestamp": orderedTestDates[1].timestamp(),
			"dirroot": "stationSaver_testUser"
		},
		{
			"pk": super_path_user_id,
			"username": "superPath_testUser",
			"displayname": "Super Pathouser",
			"hashedpw": testPassword,
			"email": "test47@test.com",
			"isdisabled": False,
			"creationtimestamp": orderedTestDates[1].timestamp(),
			"dirroot": "superPath_testUser"
		},
		{
			"pk": tossed_slash_user_id,
			"username": "tossedSlash_testUser",
			"displayname": "Tossed Slash",
			"hashedpw": testPassword,
			"email": "test48@test.com",
			"isdisabled": False,
			"creationtimestamp": orderedTestDates[1].timestamp(),
			"dirroot": "tossedSlash"
		},
		{
			"pk": unruled_station_user_id,
			"username": "unruledStation_testUser",
			"displayname": "Unruled Station User",
			"hashedpw": testPassword,
			"email": "test49@test.com",
			"isdisabled": False,
			"creationtimestamp": orderedTestDates[1].timestamp(),
			"dirroot": "unruledStation"
		}
	]
	return users_params

def get_user_role_params(
	orderedTestDates: List[datetime],
	primaryUser: AccountInfo,
) -> list[dict[Any, Any]]:
	return [
		{
			"userfk": primaryUser.id,
			"role": UserRoleDef.ADMIN.value,
			"creationtimestamp": orderedTestDates[0].timestamp(),
			"span": 0,
			"count": 0,
			"priority": None
		},
		{
			"userfk": golf_user_id,
			"role": UserRoleDef.USER_LIST.value,
			"creationtimestamp": orderedTestDates[0].timestamp(),
			"span": 0,
			"count": 0,
			"priority": None
		}
	]



def get_actions_history(
	orderedTestDates: List[datetime]
) -> list[dict[Any, Any]]:

	return [
	]
