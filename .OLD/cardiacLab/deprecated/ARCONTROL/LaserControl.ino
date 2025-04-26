// TODO Add time control to the arduino, if time exceeds the restriction turn off laser until x number of seconds,
// DONE 30min break

// FIXME better to have two arduinos together, one controls laser, the other one controls communications
// TODO create a new fuction that groups everythin, code too long that does the same thing multiple times

/**
 * Variables for laser waveform 
 */

struct laserData
{
    String name;
    bool trigger; // fix to bool
};

struct laserTrigger
{
    unsigned long millis; // millis() returns an unsigned long.
    bool state;           // state variable for the LED
};

struct currentTrigger
{
    unsigned long millis;
    bool state;
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
// char receivedChars[] = "OneLaser-0,TwoLaser-0,ThreeLaser-0,FourLaser-0"; // test variable

char laserText[32] = {0}; // general variable

int laserState = 0;
unsigned long plaserMillis = 0; // millis() returns an unsigned long.
float slaserMillis = 0.0;       // seconds
/**
 * all variables to indicate laser
 */
char laser01Str[32] = {0};
char laser02Str[32] = {0};
char laser03Str[32] = {0};
char laser04Str[32] = {0};

int laser01Pin = 2;
int laser02Pin = 3;
int laser03Pin = 4;
int laser04Pin = 5;

bool laserState01 = false; // state variable for the LED
bool laserState02 = false; // state variable for the LED
bool laserState03 = false; // state variable for the LED
bool laserState04 = false; // state variable for the LED

String mystring(laserText);

String one = String("OneLaser");
String two = String("TwoLaser");
String three = String("ThreeLaser");
String four = String("FourLaser");

laserData laser01Data = {mystring, laserState};
laserData laser02Data = {mystring, laserState};
laserData laser03Data = {mystring, laserState};
laserData laser04Data = {mystring, laserState};

laserTrigger laser01Trigger = {plaserMillis, false};
laserTrigger laser02Trigger = {plaserMillis, false};
laserTrigger laser03Trigger = {plaserMillis, false};
laserTrigger laser04Trigger = {plaserMillis, false};

Clock globalClocklaser01 = {slaserMillis, false};
Clock secureClocklaser01 = {slaserMillis, false};
Clock globalClocklaser02 = {slaserMillis, false};
Clock secureClocklaser02 = {slaserMillis, false};
Clock globalClocklaser03 = {slaserMillis, false};
Clock secureClocklaser03 = {slaserMillis, false};
Clock globalClocklaser04 = {slaserMillis, false};
Clock secureClocklaser04 = {slaserMillis, false};

unsigned long interval = 250; // 2Hz the time we need to wait
float intervalGlob = 15.0;    // One minute on One minute
float intervalSecure = 60.0;  // maybe one minute in seconds? 1800

void setup()
{
    Serial.begin(9600);
    Serial.println("<Arduino is ready>");
    laserSetUp(); // set up laser
    // showParsedData();
}

void loop()
{
    unsigned long current = millis(); // grab current time
    // float newcurrent = (float)(millis() / 1000);
    // Serial.println(newcurrent);

    if (Serial.available() > 0)
    {
        // read the incoming byte:
        incomingData = Serial.readString();
        char incomingString[50];
        incomingData.toCharArray(incomingString, 50);

        char *strtokIndx; // this is used by strtok() as an index

        strtokIndx = strtok(incomingString, ","); // get the first part - the string
        strcpy(laser01Str, strtokIndx);           // copy it to laserName
        strtokIndx = strtok(NULL, ",");           // this continues where the previous call left off
        strcpy(laser02Str, strtokIndx);           // copy it to laserName
        strtokIndx = strtok(NULL, ",");           // get the first part - the string
        strcpy(laser03Str, strtokIndx);           // copy it to laserName
        strtokIndx = strtok(NULL, ",");           // this continues where the previous call left off
        strcpy(laser04Str, strtokIndx);           // copy it to laserName

        // add only update if laser state changes!!!!!!!!!!!!!!!!!!
        laserData laser01Datapre = parseLaser(laser01Str); // individual
        laserData laser02Datapre = parseLaser(laser02Str); // individual
        laserData laser03Datapre = parseLaser(laser03Str); // individual
        laserData laser04Datapre = parseLaser(laser04Str); // individual

        if (laser01Datapre.trigger != laser01Data.trigger)
        {
            laser01Data = laser01Datapre;
            secureClocklaser01 = updateVals(laser01Data.trigger);
            globalClocklaser01 = updateVals(laser01Data.trigger);
        }

        if (laser02Datapre.trigger != laser02Data.trigger)
        {
            laser02Data = laser02Datapre;
            secureClocklaser02 = updateVals(laser02Data.trigger);
            globalClocklaser02 = updateVals(laser02Data.trigger);
        }

        if (laser03Datapre.trigger != laser03Data.trigger)
        {
            laser03Data = laser03Datapre;
            secureClocklaser03 = updateVals(laser03Data.trigger);
            globalClocklaser03 = updateVals(laser03Data.trigger);
        }

        if (laser04Datapre.trigger != laser04Data.trigger)
        {
            laser04Data = laser04Datapre;
            secureClocklaser04 = updateVals(laser04Data.trigger);
            globalClocklaser04 = updateVals(laser04Data.trigger);
        }
    }

    // if (laser01Data.trigger == 1)
    // {
    //     currentTrigger vlaser01 = square_wave(current, laser01Trigger.millis, laser01Trigger.state, laser01Pin);
    //     laser01Trigger.millis = vlaser01.millis;
    //     laser01Trigger.state = vlaser01.state;
    // }
    // else if (laser01Data.trigger == 0)
    // {
    //     digitalWrite(laser01Pin, false);
    // }

    /** 
 * timer stimulation, control over the stim protocol, maybe group this in a function?? 
 * #FIXME try to make this into a function, do more research C++
 * #NOTE Right now all the windows are the same size (maybe adjust for later?)
 */
    // LASER 01
    if (laser01Data.trigger == true)
    {
        // First clock protects agains long stimulation
        secureClocklaser01 = timer(current, secureClocklaser01.millis, secureClocklaser01.clockstate, intervalSecure);

        if (secureClocklaser01.clockstate == true)
        {
            // Second clock adjusts stimulation protocol
            globalClocklaser01 = timer(current, globalClocklaser01.millis, globalClocklaser01.clockstate, intervalGlob);

            if (globalClocklaser01.clockstate == true)
            {
                // third clock regulates pulse generation
                laser01Trigger = square_wave(current, laser01Trigger.millis, laser01Trigger.state, laser01Pin, interval);
            }

            else if (globalClocklaser01.clockstate == false)
            {
                digitalWrite(laser01Pin, false);
            }
        }
        else if (secureClocklaser01.clockstate == false)
        {
            digitalWrite(laser01Pin, false);
            globalClocklaser01 = updateVals(laser01Data.trigger);
        }
    }

    else if (laser01Data.trigger == false)
    {
        // maybe create function to reset all clocks?
        secureClocklaser01.millis = slaserMillis;
        secureClocklaser01.clockstate = false;
        globalClocklaser01.millis = slaserMillis;
        globalClocklaser01.clockstate = false;
        laser01Trigger.millis = plaserMillis;
        laser01Trigger.state = false;
        digitalWrite(laser01Pin, false);
    }

    // LASER 02
    if (laser02Data.trigger == true)
    {
        // First clock protects agains long stimulation
        secureClocklaser02 = timer(current, secureClocklaser02.millis, secureClocklaser02.clockstate, intervalSecure);

        if (secureClocklaser02.clockstate == true)
        {
            // Second clock adjusts stimulation protocol
            globalClocklaser02 = timer(current, globalClocklaser02.millis, globalClocklaser02.clockstate, intervalGlob);

            if (globalClocklaser02.clockstate == true)
            {
                // third clock regulates pulse generation
                laser02Trigger = square_wave(current, laser02Trigger.millis, laser02Trigger.state, laser02Pin, interval);
            }

            else if (globalClocklaser02.clockstate == false)
            {
                digitalWrite(laser02Pin, false);
            }
        }
        else if (secureClocklaser02.clockstate == false)
        {
            digitalWrite(laser02Pin, false);
            globalClocklaser02 = updateVals(laser02Data.trigger);
        }
    }

    else if (laser02Data.trigger == false)
    {
        // maybe create function to reset all clocks?
        secureClocklaser02.millis = slaserMillis;
        secureClocklaser02.clockstate = false;
        globalClocklaser02.millis = slaserMillis;
        globalClocklaser02.clockstate = false;
        laser02Trigger.millis = plaserMillis;
        laser02Trigger.state = false;
        digitalWrite(laser02Pin, false);
    }
    // LASER 03
    if (laser03Data.trigger == true)
    {
        // First clock protects agains long stimulation
        secureClocklaser03 = timer(current, secureClocklaser03.millis, secureClocklaser03.clockstate, intervalSecure);

        if (secureClocklaser03.clockstate == true)
        {
            // Second clock adjusts stimulation protocol
            globalClocklaser03 = timer(current, globalClocklaser03.millis, globalClocklaser03.clockstate, intervalGlob);

            if (globalClocklaser03.clockstate == true)
            {
                // third clock regulates pulse generation
                laser03Trigger = square_wave(current, laser03Trigger.millis, laser03Trigger.state, laser03Pin, interval);
            }

            else if (globalClocklaser03.clockstate == false)
            {
                digitalWrite(laser03Pin, false);
            }
        }
        else if (secureClocklaser03.clockstate == false)
        {
            digitalWrite(laser03Pin, false);
            globalClocklaser03 = updateVals(laser03Data.trigger);
        }
    }

    else if (laser03Data.trigger == false)
    {
        // maybe create function to reset all clocks?
        secureClocklaser03.millis = slaserMillis;
        secureClocklaser03.clockstate = false;
        globalClocklaser03.millis = slaserMillis;
        globalClocklaser03.clockstate = false;
        laser03Trigger.millis = plaserMillis;
        laser03Trigger.state = false;
        digitalWrite(laser03Pin, false);
    }
    // LASER 04
    if (laser04Data.trigger == true)
    {
        // First clock protects agains long stimulation
        secureClocklaser04 = timer(current, secureClocklaser04.millis, secureClocklaser04.clockstate, intervalSecure);

        if (secureClocklaser04.clockstate == true)
        {
            // Second clock adjusts stimulation protocol
            globalClocklaser04 = timer(current, globalClocklaser04.millis, globalClocklaser04.clockstate, intervalGlob);

            if (globalClocklaser04.clockstate == true)
            {
                // third clock regulates pulse generation
                laser04Trigger = square_wave(current, laser04Trigger.millis, laser04Trigger.state, laser04Pin, interval);
            }

            else if (globalClocklaser04.clockstate == false)
            {
                digitalWrite(laser04Pin, false);
            }
        }
        else if (secureClocklaser04.clockstate == false)
        {
            digitalWrite(laser04Pin, false);
            globalClocklaser04 = updateVals(laser04Data.trigger);
        }
    }

    else if (laser04Data.trigger == false)
    {
        // maybe create function to reset all clocks?
        secureClocklaser04.millis = slaserMillis;
        secureClocklaser04.clockstate = false;
        globalClocklaser04.millis = slaserMillis;
        globalClocklaser04.clockstate = false;
        laser04Trigger.millis = plaserMillis;
        laser04Trigger.state = false;
        digitalWrite(laser04Pin, false);
    }
}

void laserSetUp()
{

    pinMode(laser01Pin, OUTPUT);
    pinMode(laser02Pin, OUTPUT);
    pinMode(laser03Pin, OUTPUT);
    pinMode(laser04Pin, OUTPUT);

    digitalWrite(laser01Pin, true);
    digitalWrite(laser02Pin, true);
    digitalWrite(laser03Pin, true);
    digitalWrite(laser04Pin, true);
    delay(1000);
    digitalWrite(laser01Pin, laserState01);
    digitalWrite(laser02Pin, laserState02);
    digitalWrite(laser03Pin, laserState03);
    digitalWrite(laser04Pin, laserState04);
}

/**
 * Split the transmitted string  
 */

struct laserData parseLaser(char *receivedLaser)
{
    char *strtokIndx2; // this is used by strtok() as an index

    strtokIndx2 = strtok(receivedLaser, "-"); // get the first part - the string
    strcpy(laserText, strtokIndx2);           // copy it to laserText

    strtokIndx2 = strtok(NULL, "-"); // this continues where the previous call left off
    laserState = atoi(strtokIndx2);  // convert this part to an integer

    String mystring(laserText);
    return {laserText, laserState};
}

// print received variables

void showParsedData(String Name, int State)
{
    Serial.print("Laser ");
    Serial.println(Name);
    Serial.print("State ");
    Serial.println(State);
}

// function to create a square wave

struct laserTrigger square_wave(unsigned long currentMillis, unsigned long previousMillis, bool ledState, int PinNumber, unsigned long intervalSquare)
{
    if ((unsigned long)(currentMillis - previousMillis) >= intervalSquare)
    {
        ledState = !ledState;              // "toggles" the state
        digitalWrite(PinNumber, ledState); // sets the LED based on ledState
        // save the "current" time
        return {millis(), ledState};
    }
    return {previousMillis, ledState};
}

// function to control time

struct Clock timer(unsigned long currentMillis, float previousMillis, bool StateClock, float ClockInterval)
{
    if ((float)((currentMillis / 1000) - previousMillis) >= ClockInterval)
    {
        StateClock = !StateClock; // "toggles" the state
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