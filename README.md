Things that (I believe?) will need to happen:

1) Since we want essentially a peer-to-peer communication system,
each program (rover.c, drone.c) will need both a listening and sending socket.
2) Also realised that the listening call is a blocking funciton, so we may need
to multithread this program?
  Actually no threading please: https://steelkiwi.com/blog/working-tcp-sockets/
