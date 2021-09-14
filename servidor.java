import java.io.IOException;
import java.net.ServerSocket;
import java.net.Socket;
import java.util.Scanner;

public class servidor {
  public static void main(String[] args) throws IOException {
    ServerSocket servidor = new ServerSocket(65432);
    System.out.println("Porta 65432 aberta!");

    Socket cliente = servidor.accept();
    System.out.println("Nova conexão com o cliente " + cliente.getInetAddress().getHostAddress());

    Scanner s = new Scanner(cliente.getInputStream());
    while (s.hasNextLine()) {
      System.out.println(s.nextLine());
    }

    s.close();
    servidor.close();
    cliente.close();
  }
}