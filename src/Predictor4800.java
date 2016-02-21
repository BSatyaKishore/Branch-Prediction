// Alpha 21264 (EV6) Hybrid Predictor
// Gshare
//  Pap
import java.math.*;

public class Predictor4800 extends Predictor {
	Table main_table; // = new Table(1400,1);
	Table GHR;
	// Table GHR2;
	// BigInteger bi;
	String bi;
	// assign values to bi1, bi2
	public Predictor4800() {
		main_table = new Table(2048,2);
		// main_table = new Table()
		GHR = new Table(256,2);
		// GHR2 = new Table(12,3);
	}


	public void Train(long address, boolean outcome, boolean predict) {

		long n = address%512;
		long n1 = address%256;
		int a = (int) n;
		int b = (int) n1;
		int pk = GHR.getInteger(b,0,1);
		int outcomei = outcome ? 1 :0;

		// int p3 = Past.getInteger(0,0);
		a = (a << 2) + pk;
		pk = ((pk<<1)+outcomei)%4;
		int pt = main_table.getInteger(a,0,1);
		if(outcome){
			if(pt<3){
				pt++;
			}
		}
		else{
			if(pt>0){
				pt--;
			}
		}
		// // main_table
		main_table.setInteger(a,0,1,pt);
		GHR.setInteger(b,0,1,pk);
	}


	public boolean predict(long address){
		long n = address%512;
		long n1 = address%256;
		int a = (int) n;
		int b = (int) n1;
		int p2 = GHR.getInteger(b,0,1);
		// System.out.println(p2+"p"+a+"a"+n+"n");
		a = (a << 2) + p2;
		// System.out.println(a);
		int p1 = main_table.getInteger(a,0,1);
		return p1 >1;
	}

}
