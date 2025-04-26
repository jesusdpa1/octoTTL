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

/**
 * variables to received from python 
 */
String incomingData;
char receivedChars[] = "OneLaser-0,TwoLaser-0,ThreeLaser-0,FourLaser-0"; // test variable

char laserText[32] = {0}; // general variable

unsigned long plaserMillis = 0; // millis() returns an unsigned long.
float slaserMillis = 0.0;       // seconds
unsigned long intervalSquare = 1000;
/**
 * all variables to indicate laser
 */
char pythonStr01[32] = {0};
char pythonStr02[32] = {0};
char pythonStr03[32] = {0};
char pythonStr04[32] = {0};

int controlPin01 = 2;
int controlPin02 = 3;
int controlPin03 = 4;
int controlPin04 = 5;
int arpyON = 7;

String mystring(laserText);

String one = String("OneLaser");
String two = String("TwoLaser");
String three = String("ThreeLaser");
String four = String("FourLaser");

receivedData pythonData01 = {mystring, false};
receivedData pythonData02 = {mystring, false};
receivedData pythonData03 = {mystring, false};
receivedData pythonData04 = {mystring, false};

bool pythonTrigger01 = false;
bool pythonTrigger02 = false;
bool pythonTrigger03 = false;
bool pythonTrigger04 = false;
// triggerData pythonTrigger01 = {false, false};
// triggerData pythonTrigger02 = {false, false};
// triggerData pythonTrigger03 = {false, false};
// triggerData pythonTrigger04 = {false, false};

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
    // showParsedData();
}

void loop()
{
    digitalWrite(arpyON, true);
    if (Serial.available() > 0)
    {
        // read the incoming byte:
        incomingData = Serial.readString();
        char incomingString[50];
        incomingData.toCharArray(incomingString, 50);

        char *strtokIndx; // this is used by strtok() as an index

        strtokIndx = strtok(incomingString, ","); // get the first part - the string
        strcpy(pythonStr01, strtokIndx);          // copy it to laserName
        strtokIndx = strtok(NULL, ",");           // this continues where the previous call left off
        strcpy(pythonStr02, strtokIndx);          // copy it to laserName
        strtokIndx = strtok(NULL, ",");           // get the first part - the string
        strcpy(pythonStr03, strtokIndx);          // copy it to laserName
        strtokIndx = strtok(NULL, ",");           // this continues where the previous call left off
        strcpy(pythonStr04, strtokIndx);          // copy it to laserName

        // add only update if laser state changes!!!!!!!!!!!!!!!!!!
        receivedData pythonDatapre01 = parseLaser(pythonStr01); // individual
        receivedData pythonDatapre02 = parseLaser(pythonStr02); // individual
        receivedData pythonDatapre03 = parseLaser(pythonStr03); // individual
        receivedData pythonDatapre04 = parseLaser(pythonStr04); // individual

        // LASER 01
        if (pythonDatapre01.trigger != pythonData01.trigger)
        {
            pythonData01 = pythonDatapre01;
            pythonTrigger01 = true;
            // pythonTrigger01 = triggerControl(pythonData01.trigger, pythonTrigger01.triggerOFF, pythonTrigger01.triggerON);
        }
        else if (pythonDatapre01.trigger == pythonData01.trigger)
        {
            pythonTrigger01 = false;
        }

        // LASER 02
        if (pythonDatapre02.trigger != pythonData02.trigger)
        {
            pythonData02 = pythonDatapre02;
            pythonTrigger02 = true;
            // pythonTrigger01 = triggerControl(pythonData01.trigger, pythonTrigger01.triggerOFF, pythonTrigger01.triggerON);
        }
        else if (pythonDatapre02.trigger == pythonData02.trigger)
        {
            pythonTrigger02 = false;
        }

        // LASER 03
        if (pythonDatapre03.trigger != pythonData03.trigger)
        {
            pythonData03 = pythonDatapre03;
            pythonTrigger03 = true;
            // pythonTrigger01 = triggerControl(pythonData01.trigger, pythonTrigger01.triggerOFF, pythonTrigger01.triggerON);
        }
        else if (pythonDatapre03.trigger == pythonData03.trigger)
        {
            pythonTrigger03 = false;
        }
        // LASER 04
        if (pythonDatapre04.trigger != pythonData04.trigger)
        {
            pythonData04 = pythonDatapre04;
            pythonTrigger04 = true;
            // pythonTrigger01 = triggerControl(pythonData01.trigger, pythonTrigger01.triggerOFF, pythonTrigger01.triggerON);
        }
        else if (pythonDatapre04.trigger == pythonData04.trigger)
        {
            pythonTrigger04 = false;
        }

        unsigned long current = millis(); // grab current time
        unsigned long previousMillis = millis();
        while ((unsigned long)(current - previousMillis) <= intervalSquare)
        {
            // Laser01
            digitalWrite(controlPin01, pythonTrigger01);
            digitalWrite(controlPin02, pythonTrigger02);
            digitalWrite(controlPin03, pythonTrigger03);
            digitalWrite(controlPin04, pythonTrigger04);
            current = millis();
        }
        digitalWrite(controlPin01, false);
        digitalWrite(controlPin02, false);
        digitalWrite(controlPin03, false);
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