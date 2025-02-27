-- Keep a log of any SQL queries you execute as you solve the mystery.

--search description from crime scenes at Humphrey Street on July 28, 2023

SELECT description FROM crime_scene_reports WHERE year = 2023 AND month = 7 AND day = 28 AND street = 'Humphrey Street';

--time: 10:15am Humphrey Street Backery, 3 witness, interviews mentions backery, should probably check the interviews

SELECT transcript FROM interviews WHERE year = 2023 AND month = 7 AND day = 28;

--| “Ah,” said he, “I forgot that I had not seen you for some weeks. It is a little souvenir from the King of Bohemia in return for my assistance in the case of the Irene Adler papers.”                                                                                                                               |
--| “I suppose,” said Holmes, “that when Mr. Windibank came back from France he was very annoyed at your having gone to the ball.”                                                                                                                                                                                      |
--| “You had my note?” he asked with a deep harsh voice and a strongly marked German accent. “I told you that I would call.” He looked from one to the other of us, as if uncertain which to address.                                                                                                                   |
--| Sometime within ten minutes of the theft, I saw the thief get into a car in the bakery parking lot and drive away. If you have security footage from the bakery parking lot, you might want to look for cars that left the parking lot in that time frame.                                                          |
--| I don't know the thief's name, but it was someone I recognized. Earlier this morning, before I arrived at Emma's bakery, I was walking by the ATM on Leggett Street and saw the thief there withdrawing some money.                                                                                                 |
--| As the thief was leaving the bakery, they called someone who talked to them for less than a minute. In the call, I heard the thief say that they were planning to take the earliest flight out of Fiftyville tomorrow. The thief then asked the person on the other end of the phone to purchase the flight ticket. |
|-- Our neighboring courthouse has a very annoying rooster that crows loudly at 6am every day. My sons Robert and Patrick took the rooster to a city far, far away, so it may never bother us again. My sons have successfully arrived in Paris.

--only 3 seems relavent
--| Sometime within ten minutes of the theft, I saw the thief get into a car in the bakery parking lot and drive away.
--If you have security footage from the bakery parking lot, you might want to look for cars that left the parking lot in that time frame.
                                                          |
--| I don't know the thief's name, but it was someone I recognized. Earlier this morning, before I arrived at Emma's bakery,
--I was walking by the ATM on Leggett Street and saw the thief there withdrawing some money
.                                                                                                 |
--| As the thief was leaving the bakery, they called someone who talked to them for less than a minute. In the call,
--I heard the thief say that they were planning to take the earliest flight out of Fiftyville tomorrow.
--The thief then asked the person on the other end of the phone to purchase the flight ticket. |

--Check parking lot first
SELECT license_plate, hour, minute FROM bakery_security_logs WHERE year = 2023 AND month = 7 AND day = 28 and hour = 10 AND (minute >= 15 AND minute <= 25) ORDER BY minute;

--| license_plate | hour | minute |
--+---------------+------+--------+
--| 5P2BI95       | 10   | 16     |
--| 94KL13X       | 10   | 18     |
--| 6P58WS2       | 10   | 18     |
--| 4328GD8       | 10   | 19     |
--| G412CB7       | 10   | 20     |
--| L93JTIZ       | 10   | 21     |
--| 322W7JE       | 10   | 23     |
--| 0NTHK55       | 10   | 23     |

--using the license plate, we can track down a bunch of suspects within this time frame

SELECT id, name, phone_number, passport_number FROM people where license_plate in (SELECT license_plate FROM bakery_security_logs WHERE year = 2023 AND month = 7 AND day = 28 and hour = 10 AND (minute >= 15 AND minute <= 25));

/*+--------+---------+----------------+-----------------+
|   id   |  name   |  phone_number  | passport_number |
+--------+---------+----------------+-----------------+
| 221103 | Vanessa | (725) 555-4692 | 2963008352      |
| 243696 | Barry   | (301) 555-4174 | 7526138472      |
| 396669 | Iman    | (829) 555-5269 | 7049073643      |
| 398010 | Sofia   | (130) 555-0289 | 1695452385      |
| 467400 | Luca    | (389) 555-5198 | 8496433585      |
| 514354 | Diana   | (770) 555-1861 | 3592750733      |
| 560886 | Kelsey  | (499) 555-9472 | 8294398571      |
| 686048 | Bruce   | (367) 555-5533 | 5773159633      |
+--------+---------+----------------+-----------------+*/

--this is the short list of people which are from the first interview

--This clue is now dead. Now we follow the atm from the second interview
SELECT account_number FROM atm_transactions WHERE year = 2023 AND month = 7 AND day = 28 AND atm_location = 'Leggett Street' AND transaction_type = 'withdraw';

/*+----------------+------------------+
| account_number | transaction_type |
+----------------+------------------+
| 28500762       | withdraw         |
| 28296815       | withdraw         |
| 76054385       | withdraw         |
| 49610011       | withdraw         |
| 16153065       | withdraw         |
| 86363979       | deposit          |
| 25506511       | withdraw         |
| 81061156       | withdraw         |
| 26013199       | withdraw         |
+----------------+------------------+*/

--using the account number, short list suspects which is within the domain of the 1st and 2nd interview

SELECT id, name, phone_number, passport_number FROM people
where license_plate in (SELECT license_plate FROM bakery_security_logs WHERE year = 2023 AND month = 7 AND day = 28 and hour = 10 AND (minute >= 15 AND minute <= 25))
AND id in (SELECT person_id FROM bank_accounts
WHERE account_number IN (SELECT account_number FROM atm_transactions
WHERE year = 2023 AND month = 7 AND day = 28 AND atm_location = 'Leggett Street' AND transaction_type = 'withdraw'));

/*+--------+-------+----------------+-----------------+
|   id   | name  |  phone_number  | passport_number |
+--------+-------+----------------+-----------------+
| 396669 | Iman  | (829) 555-5269 | 7049073643      |
| 467400 | Luca  | (389) 555-5198 | 8496433585      |
| 514354 | Diana | (770) 555-1861 | 3592750733      |
| 686048 | Bruce | (367) 555-5533 | 5773159633      |
+--------+-------+----------------+-----------------+*/

--The above table is the short list from interview 1 and 2. Now we check call from interview 3.

SELECT caller, receiver, duration FROM phone_calls WHERE year = 2023 AND month = 7 AND day = 28 AND duration <= 60;

/*+----------------+----------------+----------+
|     caller     |    receiver    | duration |
+----------------+----------------+----------+
| (130) 555-0289 | (996) 555-8899 | 51       |
| (499) 555-9472 | (892) 555-8872 | 36       |
| (367) 555-5533 | (375) 555-8161 | 45       |
| (609) 555-5876 | (389) 555-5198 | 60       |
| (499) 555-9472 | (717) 555-1342 | 50       |
| (286) 555-6063 | (676) 555-6554 | 43       |
| (770) 555-1861 | (725) 555-3243 | 49       |
| (031) 555-6622 | (910) 555-3251 | 38       |
| (826) 555-1652 | (066) 555-9701 | 55       |
| (338) 555-6650 | (704) 555-2131 | 54       |
+----------------+----------------+----------+*/

--See who on the short list called during that day

SELECT id, name, phone_number, passport_number FROM people
where license_plate in (SELECT license_plate FROM bakery_security_logs WHERE year = 2023 AND month = 7 AND day = 28 and hour = 10 AND (minute >= 15 AND minute <= 25))
AND (phone_number IN (SELECT caller FROM phone_calls WHERE year = 2023 AND month = 7 AND day = 28 AND duration <= 60))
AND id in (SELECT person_id FROM bank_accounts
WHERE account_number IN (SELECT account_number FROM atm_transactions
WHERE year = 2023 AND month = 7 AND day = 28 AND atm_location = 'Leggett Street' AND transaction_type = 'withdraw'));

/*+--------+-------+----------------+-----------------+
|   id   | name  |  phone_number  | passport_number |
+--------+-------+----------------+-----------------+
| 514354 | Diana | (770) 555-1861 | 3592750733      |
| 686048 | Bruce | (367) 555-5533 | 5773159633      |
+--------+-------+----------------+-----------------+*/

--Find out their receiver:
SELECT caller, receiver, duration FROM phone_calls WHERE year = 2023 AND month = 7 AND day = 28 AND duration <= 60 AND caller IN (SELECT phone_number FROM people
where license_plate in (SELECT license_plate  FROM bakery_security_logs WHERE year = 2023 AND month = 7 AND day = 28 and hour = 10 AND (minute >= 15 AND minute <= 25))
AND (phone_number IN (SELECT caller FROM phone_calls WHERE year = 2023 AND month = 7 AND day = 28 AND duration <= 60))
AND id in (SELECT person_id FROM bank_accounts
WHERE account_number IN (SELECT account_number FROM atm_transactions
WHERE year = 2023 AND month = 7 AND day = 28 AND atm_location = 'Leggett Street' AND transaction_type = 'withdraw')));

/*+----------------+----------------+----------+
|     caller     |    receiver    | duration |
+----------------+----------------+----------+
| (367) 555-5533 | (375) 555-8161 | 45       |
| (770) 555-1861 | (725) 555-3243 | 49       |
+----------------+----------------+----------+*/

--Now Check Flight

SELECT destination_airport_id, id, hour, minute FROM flights WHERE year = 2023 AND month = 7 AND day = 29 ORDER BY hour, minute;

/*+------------------------+----+------+--------+
| destination_airport_id | id | hour | minute |
+------------------------+----+------+--------+
| 4                      | 36 | 8    | 20     |
| 1                      | 43 | 9    | 30     |
| 11                     | 23 | 12   | 15     |
| 9                      | 53 | 15   | 20     |
| 6                      | 18 | 16   | 0      |
+------------------------+----+------+--------+*/

--only 5 flights, check these 5 flights to see if they have the passport of the suspect

SELECT passport_number, flight_id FROM passengers WHERE flight_id IN(SELECT id FROM flights WHERE year = 2023 AND month = 7 AND day = 29) AND (passport_number = 3592750733 OR passport_number = 5773159633);

/*+-----------------+-----------+
| passport_number | flight_id |
+-----------------+-----------+
| 3592750733      | 18        |
| 5773159633      | 36        |*/

--According to interview 3, they should take the earlier flight possible. Hence, flight_id 36 should be the flight they attended. Using the passport number, Bruce is the thief.
--Using diana's number and the receiver of her phone call number, we can track down the assistant.

SELECT name FROM people WHERE phone_number = '(375) 555-8161';

/*+-------+
| name  |
+-------+
| Robin |
+-------+*/

--Robin is the assistant
--Using fght_id of 36 and the previous table of destination airport id off 4, we can track down the city they escaped to:

SELECT city FROM airports WHERE id = 4;

--New York City is the destination
