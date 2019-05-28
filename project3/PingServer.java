import java.io.*;
import java.net.*;
import java.util.*;

/**
 * Server to process ping requests over UDP.
 */
public class PingServer {

  /**
   * Ping handler thread.
   */
  private static class Pong extends Thread {
    DatagramPacket ping;
    Random random;
    double lossRate;
		double bitErrorRate;
    int avgDelay;

    Pong(DatagramPacket ping, Random random, double lossRate, double bitErrorRate, int avgDelay) {
      this.ping = ping;
      this.random = random;
      this.lossRate = lossRate;
      this.bitErrorRate = bitErrorRate;
      this.avgDelay = avgDelay;
    }

    public void run() {
      try {
        // Print the received data.
        printData(ping);

        // Decide whether to reply, or simulate packet loss.
        if (random.nextDouble() < lossRate) {
          System.out.println("   Reply not sent.");
	        return; 
        }

        // Simulate network delay.
        Thread.sleep((int) (random.nextDouble() * 2 * avgDelay));

        // Send reply.
        InetAddress clientHost = ping.getAddress();
        int clientPort = ping.getPort();
        PingMessage pingMsg = PingMessage.fromBytes(ping.getData());
				// Validate echo request.
				if (pingMsg.getType() != 8) {
					System.err.println("WARNING: echo request has wrong type=" + pingMsg.getType());
				}
				if (!pingMsg.verifyChecksum()) {
					System.err.println("WARNING: checksum verification failure for echo request seqno=" + pingMsg.getSeqNo());
				}
				PingMessage pongMsg = new PingMessage(0, 0, pingMsg.getId(), pingMsg.getSeqNo(), pingMsg.getTimestamp());
        // Decide whether or not to simulate bit errors with invalid checksum.
        if (random.nextDouble() > bitErrorRate) {
				  pongMsg.setChecksum();
        } else {
					System.out.println("   Reply has invalid checksum.");
				}
				byte[] replyBuf = pongMsg.toBytes();
        DatagramPacket reply = new DatagramPacket(replyBuf, replyBuf.length, clientHost, clientPort);
        DatagramSocket socket = new DatagramSocket();
        socket.send(reply);

        System.out.println("   Reply sent.");
      } catch (IOException | InterruptedException e) {
        System.err.println("Error processing ping request: " + e.getMessage());
      }
    }
  }

  public static void main(String[] argv) {
    // Server port.
    int port = -1;
    double lossRate = 0.3;
		double bitErrorRate = 0.1;
    int avgDelay = 100;

    // Process command-line arguments.
    for (String arg : argv) {
      String[] splitArg = arg.split("=");
      if (splitArg.length == 2 && splitArg[0].equals("--port")) {
        port = Integer.parseInt(splitArg[1]);
      } else if (splitArg.length == 2 && splitArg[0].equals("--loss_rate")) {
        lossRate = Double.parseDouble(splitArg[1]);
      } else if (splitArg.length == 2 && splitArg[0].equals("--bit_error_rate")) {
        bitErrorRate = Double.parseDouble(splitArg[1]);
      } else if (splitArg.length == 2 && splitArg[0].equals("--avg_delay")) {
        avgDelay = Integer.parseInt(splitArg[1]);
      } else {
        System.err.println("Usage: java PingServer --port=<port> [--loss_rate=<rate>] [--bit_error_rate=<rate>] [--avg_delay=<delay>]");
        return;
      }
    }

    // Check port number.
    if (port == -1) {
      System.err.println("Must specify port number with --port");
      return;
    }
    if (port <= 1024) {
      System.err.println("Avoid potentially reserved port number: " + port + " (should be > 1024)");
      return;
    }

    // Create random number generator for use in simulating 
    // packet loss and network delay.
    Random random = new Random();

    try {
      // Create a datagram socket for receiving and sending UDP packets
      // through the port specified on the command line.
      DatagramSocket socket = new DatagramSocket(port);

      System.out.println("Ping server listening on UDP port " + port + " ...");

      // Processing loop.
      while (true) {
        // Create a datagram packet to hold incomming UDP packet.
        DatagramPacket request = new DatagramPacket(new byte[PingMessage.MSG_SIZE], 0, PingMessage.MSG_SIZE);

        // Block until the host receives a UDP packet.
        socket.receive(request);
        
        // Create new thread to handle ping request.
        Pong pong = new Pong(request, random, lossRate, bitErrorRate, avgDelay);
        pong.start();
      }
    } catch (IOException e) {
      System.err.println("Error processing ping request: " + e.getMessage());
    }
  }

  /** 
   * Print ping data to the standard output stream.
   */
  private static void printData(DatagramPacket request) throws IOException {
    PingMessage pingMessage = PingMessage.fromBytes(request.getData());
		String line = "PING id:" + pingMessage.getId() + " seqno:" + pingMessage.getSeqNo() + " timestamp:" + pingMessage.getTimestamp();
    System.out.println( "Received from " +  request.getAddress().getHostAddress() + ": " + line);
  }
}
