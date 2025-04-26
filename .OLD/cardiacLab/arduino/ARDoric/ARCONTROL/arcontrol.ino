// TODO Add time control to the arduino, if time exceeds the restriction turn off laser until x number of seconds,
// DONE 30min break

// FIXME better to have two arduinos together, one controls laser, the other one controls communications
// TODO create a new fuction that groups everythin, code too long that does the same thing multiple times

/**
 * Variables for laser waveform
 */

struct receivedData
{
    String name;
    bool trigger;
};

struct triggerData
{
    bool triggerON;
    bool triggerOFF;
};

struct Clock
{
    float millis;
    bool clockstate;
};

/**
 * variables to received from python
 */

String incomingData;
char receivedChars[] = "OneLaser-0,TwoLaser-0,ThreeLaser-0,FourLaser-0"; // test variable

char laserText[32] = {0}; // general variable

/**
 * all variables to indicate laser
 */
char pythonStr01[32] = {0};
char pythonStr02[32] = {0};
char pythonStr03[32] = {0};
char pythonStr04[32] = {0};

int controlPin01 = 2;
int controlPin02 = 4;
int controlPin03 = 6;
int controlPin04 = 8;
int arpyON = 7;

bool control_input = false;
String mystring(laserText);
char incomingString[50];
String readString;

String one = String("a");
String two = String("b");
String three = String("c");
String four = String("d");

receivedData pythonData01 = {mystring, false};
receivedData pythonData02 = {mystring, false};
receivedData pythonData03 = {mystring, false};
receivedData pythonData04 = {mystring, false};

receivedData pythonDatapre = {mystring, false};

bool pythonTrigger01 = false;
bool pythonTrigger02 = false;
bool pythonTrigger03 = false;
bool pythonTrigger04 = false;

// triggerData pythonTrigger01 = {false, false};
// triggerData pythonTrigger02 = {false, false};
// triggerData pythonTrigger03 = {false, false};
// triggerData pythonTrigger04 = {false, false};

// CLOCKS FOR DYNAMIC SQUARE WAVEFORM

unsigned long plaserMillis = 0;   // millis() returns an unsigned long.
float slaserMillis = 0.0;         // seconds
unsigned long intervalSquare = 1; // 1 sec waveform

Clock ClockTrigger01 = {slaserMillis, false};
Clock ClockTrigger02 = {slaserMillis, false};
Clock ClockTrigger03 = {slaserMillis, false};
Clock ClockTrigger04 = {slaserMillis, false};

int interruptPin = 12;

void setup()
{
    Serial.begin(9600);
    Serial.println("<Arduino is ready>");
    laserSetUp(); // set up laser

    pythonData01 = {one, false};
    pythonData02 = {two, false};
    pythonData03 = {three, false};
    pythonData04 = {four, false};

    for (int i = 0; i < 3; i++)
    {
        digitalWrite(arpyON, true);
        delay(500);
        digitalWrite(arpyON, false);
        delay(500);
    }

    digitalWrite(controlPin01, false);
    digitalWrite(controlPin02, false);
    digitalWrite(controlPin03, false);
    digitalWrite(controlPin04, false);
    // showParsedData();;
}

void loop()
{
    digitalWrite(arpyON, true);
    // really important function to memorized. Serial.readString is slow...
    while (Serial.available() > 0)
    {
        char c = Serial.read();
        if (c != ';')
        {
            if (c != '\n' && c != '\r')
            {
                // Not a carriage return
                readString += c;
            }
        }
        else if (c == ';')
        {
            // A carriage return finally got here...
            readString.toCharArray(incomingString, 10);
            pythonDatapre = parseLaser(incomingString); // individual
            Serial.println(pythonDatapre.name);
            Serial.println(pythonDatapre.trigger);
            readString = "";
            control_input = false;
        }
    }

    if (pythonData01.name == pythonDatapre.name)
    {
        if (pythonData01.trigger != pythonDatapre.trigger)
        {
            pythonData01 = pythonDatapre;
            ClockTrigger01 = updateVals(true);
        }
    }

    else if (pythonData02.name == pythonDatapre.name)
    {
        if (pythonData02.trigger != pythonDatapre.trigger)
        {
            pythonData02 = pythonDatapre;
            ClockTrigger02 = updateVals(true);
        }
    }

    else if (pythonData03.name == pythonDatapre.name)
    {
        if (pythonData03.trigger != pythonDatapre.trigger)
        {
            pythonData03 = pythonDatapre;
            ClockTrigger03 = updateVals(true);
        }
    }

    else if (pythonData04.name == pythonDatapre.name)
    {
        if (pythonData04.trigger != pythonDatapre.trigger)
        {
            pythonData04 = pythonDatapre;
            ClockTrigger04 = updateVals(true);
        }
    }

    // LASER 01

    if (ClockTrigger01.clockstate == true)
    {
        unsigned long current01 = millis();
        ClockTrigger01 = timer(current01, ClockTrigger01.millis, ClockTrigger01.clockstate, intervalSquare);
        digitalWrite(controlPin01, true);
    }

    else if (ClockTrigger01.clockstate == false)
    {
        digitalWrite(controlPin01, false);
    }

    if (ClockTrigger02.clockstate == true)
    {
        unsigned long current02 = millis();
        ClockTrigger02 = timer(current02, ClockTrigger02.millis, ClockTrigger02.clockstate, intervalSquare);
        digitalWrite(controlPin02, true);
    }
    else if (ClockTrigger02.clockstate == false)
    {
        digitalWrite(controlPin02, false);
    }

    if (ClockTrigger03.clockstate == true)
    {
        unsigned long current03 = millis();
        ClockTrigger03 = timer(current03, ClockTrigger03.millis, ClockTrigger03.clockstate, intervalSquare);
        digitalWrite(controlPin03, true);
    }
    else if (ClockTrigger03.clockstate == false)
    {
        digitalWrite(controlPin03, false);
    }

    if (ClockTrigger04.clockstate == true)
    {
        unsigned long current04 = millis();
        ClockTrigger04 = timer(current04, ClockTrigger04.millis, ClockTrigger04.clockstate, intervalSquare);
        digitalWrite(controlPin04, true);
    }
    else if (ClockTrigger04.clockstate == false)
    {
        digitalWrite(controlPin04, false);
    }
}

void laserSetUp()
{

    pinMode(controlPin01, OUTPUT);
    pinMode(controlPin02, OUTPUT);
    pinMode(controlPin03, OUTPUT);
    pinMode(controlPin04, OUTPUT);
    pinMode(arpyON, OUTPUT);
    pinMode(interruptPin, OUTPUT);
}

struct receivedData parseLaser(char *receivedLaser)
{
    char *strtokIndx2; // this is used by strtok() as an index

    strtokIndx2 = strtok(receivedLaser, "-"); // get the first part - the string
    strcpy(laserText, strtokIndx2);           // copy it to laserText

    strtokIndx2 = strtok(NULL, "-");    // this continues where the previous call left off
    int laserState = atoi(strtokIndx2); // convert this part to an integer
    String mystring(laserText);

    return {laserText, laserState};
}

struct Clock timer(unsigned long currentMillis, float previousMillis, bool StateClock, float ClockInterval)
{
    if ((float)((currentMillis / 1000) - previousMillis) >= ClockInterval)
    {
        StateClock = false; // "toggles" the state
        float new_time = (float)(millis() / 1000);
        return {new_time, StateClock};
    }
    return {previousMillis, StateClock};
}

struct Clock updateVals(bool StateUpdate)
{
    if (StateUpdate == true)
    {
        float new_time = float(millis() / 1000);
        return {new_time, true};
    }
}