// DONE Add time control to the arduino, if time exceeds the restriction turn off laser until x number of seconds,
// DONE 30min break

// FIXME better to have two arduinos together, one controls laser, the other one controls communications
// TODO create a new fuction that groups everythin, code too long that does the same thing multiple times
// TODO ADD POWERTEST
/**
 * Variables for laser waveform
 */
struct ControlState
{
    bool receiving;
    bool high;
    bool low;
    bool trigger;
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

unsigned long plaserMillis = 0; // millis() returns an unsigned long.
float slaserMillis = 0.0;       // seconds
/**
 * all variables to indicate laser
 */

byte state01 = 0;
byte state02 = 0;
byte state03 = 0;
byte state04 = 0;

int laserPin01 = 14;
int laserPin02 = 15;
int laserPin03 = 16;
int laserPin04 = 17;

// start pins for the LED
int ledPin01 = 18;
int ledPin02 = 19;
int ledPin03 = 20;
int ledPin04 = 21;
// end pin for the LED

bool laserState01 = false; // state variable for the LED
bool laserState02 = false; // state variable for the LED
bool laserState03 = false; // state variable for the LED
bool laserState04 = false; // state variable for the LED

int controlPin01 = 8;
int controlPin02 = 6;
int controlPin03 = 4;
int controlPin04 = 2;

int interruptPin = 21;

ControlState controlState01 = {false, false, true, false};
ControlState controlState02 = {false, false, true, false};
ControlState controlState03 = {false, false, true, false};
ControlState controlState04 = {false, false, true, false};

laserTrigger laserTrigger01 = {plaserMillis, false};
laserTrigger laserTrigger02 = {plaserMillis, false};
laserTrigger laserTrigger03 = {plaserMillis, false};
laserTrigger laserTrigger04 = {plaserMillis, false};

Clock globalClocklaser01 = {slaserMillis, false};
Clock globalClocklaser02 = {slaserMillis, false};
Clock globalClocklaser03 = {slaserMillis, false};
Clock globalClocklaser04 = {slaserMillis, false};

Clock secureClocklaser01 = {slaserMillis, false};
Clock secureClocklaser02 = {slaserMillis, false};
Clock secureClocklaser03 = {slaserMillis, false};
Clock secureClocklaser04 = {slaserMillis, false};

unsigned long interval = 500;  // 2Hz the time we need to wait
float intervalGlob = 60.0;     // One minute on One minute 60 equals 1min
float intervalSecure = 3600.0; // One Hour Tops

void setup()
{
    Serial.begin(9600);
    Serial.println("<Wavefunction generator: Start>");
    PinSetUp(); // set up laser
    Serial.println("<     Control for Doric       >");
    Serial.println("<Wavefunction generator: Ready>");
    // pinMode(interruptPin, INPUT_PULLUP);
}
// #TODO add interrupt pin, move digital read inside of the interrupt
void loop()
{
    unsigned long current = millis(); // grab current time
    // attachInterrupt(digitalPinToInterrupt(interruptPin), getState, HIGH);
    /**
     * timer stimulation, control over the stim protocol, maybe group this in a function??
     * #NOTE Right now all the windows are the same size (maybe adjust for later?)
     */
    controlState01.receiving = digitalRead(controlPin01);
    controlState02.receiving = digitalRead(controlPin02);
    controlState03.receiving = digitalRead(controlPin03);
    controlState04.receiving = digitalRead(controlPin04);

    controlState01 = highStateDetect(controlState01.receiving, controlState01.high, controlState01.low, controlState01.trigger);
    controlState02 = highStateDetect(controlState02.receiving, controlState02.high, controlState02.low, controlState02.trigger);
    controlState03 = highStateDetect(controlState03.receiving, controlState03.high, controlState03.low, controlState03.trigger);
    controlState04 = highStateDetect(controlState04.receiving, controlState04.high, controlState04.low, controlState04.trigger);

    // LASER 01
    if (controlState01.trigger == false)
    {
        // maybe create function to reset all clocks?
        state01 = 0;
        laserTrigger01 = {plaserMillis, false};
        digitalWrite(laserPin01, false);
        digitalWrite(ledPin01, false);
    }

    else if (controlState01.trigger == true)
    {
        if (state01 == 0)
        {
            secureClocklaser01 = updateVals(controlState01.trigger);
            state01 = 1;
        }
        // First clock protects against long stimulation
        secureClocklaser01 = timer(current, secureClocklaser01.millis, secureClocklaser01.clockstate, intervalSecure);

        if (secureClocklaser01.clockstate == true)
        {
            digitalWrite(laserPin01, true);
            digitalWrite(ledPin01, true);
        }
        else if (secureClocklaser01.clockstate == false)
        {
            digitalWrite(laserPin01, false);
            digitalWrite(ledPin01, false);
        }
    }
    // LASER 01

    // LASER 02
    if (controlState02.trigger == false)
    {
        // maybe create function to reset all clocks?
        state02 = 0;
        laserTrigger02 = {plaserMillis, false};
        digitalWrite(laserPin02, false);
        digitalWrite(ledPin02, false);
    }

    else if (controlState02.trigger == true)
    {
        if (state02 == 0)
        {
            secureClocklaser02 = updateVals(controlState02.trigger);
            state02 = 1;
        }
        // First clock protects agains long stimulation
        secureClocklaser02 = timer(current, secureClocklaser02.millis, secureClocklaser02.clockstate, intervalSecure);

        if (secureClocklaser02.clockstate == true)
        {
            digitalWrite(laserPin02, true);
            digitalWrite(ledPin02, true);
        }
        else if (secureClocklaser02.clockstate == false)
        {
            digitalWrite(laserPin02, false);
            digitalWrite(ledPin02, false);
        }
    }
    // LASER 02

    // LASER 03
    if (controlState03.trigger == false)
    {
        // maybe create function to reset all clocks?
        state03 = 0;
        laserTrigger03 = {plaserMillis, false};
        digitalWrite(laserPin03, false);
        digitalWrite(ledPin03, false);
    }

    else if (controlState03.trigger == true)
    {
        if (state03 == 0)
        {
            secureClocklaser03 = updateVals(controlState03.trigger);
            state03 = 1;
        }
        // First clock protects agains long stimulation
        secureClocklaser03 = timer(current, secureClocklaser03.millis, secureClocklaser03.clockstate, intervalSecure);

        if (secureClocklaser03.clockstate == true)
        {
            // Second clock adjusts stimulation protocol
            digitalWrite(laserPin03, true);
            digitalWrite(ledPin03, true);
        }
        else if (secureClocklaser03.clockstate == false)
        {
            digitalWrite(laserPin03, false);
            digitalWrite(ledPin03, false);
        }
    }
    // LASER 03

    // LASER 04
    if (controlState04.trigger == false)
    {
        // maybe create function to reset all clocks?
        state04 = 0;
        laserTrigger04 = {plaserMillis, false};
        digitalWrite(laserPin04, false);
        digitalWrite(ledPin04, false);
    }

    else if (controlState04.trigger == true)
    {
        if (state04 == 0)
        {
            secureClocklaser04 = updateVals(controlState04.trigger);
            state04 = 1;
        }
        // First clock protects agains long stimulation
        secureClocklaser04 = timer(current, secureClocklaser04.millis, secureClocklaser04.clockstate, intervalSecure);

        if (secureClocklaser04.clockstate == true)
        {
            // Second clock adjusts stimulation protocol
            digitalWrite(laserPin04, true);
            digitalWrite(ledPin04, true);
        }
        else if (secureClocklaser04.clockstate == false)
        {
            digitalWrite(laserPin04, false);
            digitalWrite(ledPin04, false);
        }
    }
    // LASER 04
}

void getState()
{
    controlState01.receiving = digitalRead(controlPin01);
    controlState02.receiving = digitalRead(controlPin02);
    controlState03.receiving = digitalRead(controlPin03);
    controlState04.receiving = digitalRead(controlPin04);
}

void PinSetUp()
{

    pinMode(controlPin01, INPUT);
    pinMode(controlPin02, INPUT);
    pinMode(controlPin03, INPUT);
    pinMode(controlPin04, INPUT);

    pinMode(laserPin01, OUTPUT);
    pinMode(laserPin02, OUTPUT);
    pinMode(laserPin03, OUTPUT);
    pinMode(laserPin04, OUTPUT);

    pinMode(ledPin01, OUTPUT);
    pinMode(ledPin02, OUTPUT);
    pinMode(ledPin03, OUTPUT);
    pinMode(ledPin04, OUTPUT);

    for (int i = 0; i < 3; i++)
    {
        digitalWrite(ledPin01, true);
        digitalWrite(ledPin02, true);
        digitalWrite(ledPin03, true);
        digitalWrite(ledPin04, true);
        delay(500);
        digitalWrite(ledPin01, false);
        digitalWrite(ledPin02, false);
        digitalWrite(ledPin03, false);
        digitalWrite(ledPin04, false);
        delay(500);
    }
}

/**
 * Split the transmitted string
 */

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

struct ControlState highStateDetect(bool receivingPinData, bool stateHigh, bool stateLow, bool Trigger)
{
    // variables for State Change detection
    // done
    if (receivingPinData == true)
    {
        if (stateLow == true)
        {
            Trigger = true;
            stateHigh = true;
        }
        else if (stateLow == false)
        {
            Trigger = false;
            stateHigh = false;
        }
    }

    if (receivingPinData == false)
    {
        if (stateHigh == true)
        {
            stateLow = false;
        }
        if (stateHigh == false)
        {
            stateLow = true;
        }
    }

    return {receivingPinData, stateHigh, stateLow, Trigger};
}