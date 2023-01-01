#include <iostream>
#include <cstdlib>
#include <signal.h>
#include <chrono>
#include <thread>
#include "RtMidi.h"
bool done;
static void finish(int ignore){ done = true; }
int main()
{
  RtMidiIn *midiin = new RtMidiIn();
  std::vector<unsigned char> message;
  int nBytes, i;
  double stamp;
  // Check available ports.
  unsigned int nPorts = midiin->getPortCount();
  std::cout << nPorts << " ports available\n";
  if ( nPorts == 0 ) {
    std::cout << "No ports available!\n";
    goto cleanup;
  }
  midiin->openPort( 1 );
  // Don't ignore sysex, timing, or active sensing messages.
  midiin->ignoreTypes( false, false, false );
  // Install an interrupt handler function.
  done = false;
  (void) signal(SIGINT, finish);

  // Periodically check input queue.
  std::cout << "Reading MIDI from port ... quit with Ctrl-C.\n";
  while ( !done ) {
    stamp = midiin->getMessage( &message );
    nBytes = message.size();
    if (nBytes > 0) {
      // Extract the note and velocity from the MIDI message
      int note = message[1];
      int velocity = message[2];
      std::cout << "Note = " << note << ", Velocity = " << velocity << ", stamp = " << stamp << std::endl;
    }
    // Sleep for 10 milliseconds ... platform-dependent.
    std::this_thread::sleep_for(std::chrono::milliseconds(10));
  }

  // Clean up
 cleanup:
  delete midiin;
  return 0;
}
