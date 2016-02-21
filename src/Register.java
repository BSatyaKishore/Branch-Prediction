

public class Register {
	private int numBits;
	private boolean value[];
	
	public Register(int bits) {
		numBits=bits;
		value=new boolean[bits];	
		Main.size+=numBits;	
	}
	
	public boolean getBitAtIndex(int bitIndex){
		return value[bitIndex];
	}
	
	public void setBitAtIndex(int bitIndex,boolean val){
		value[bitIndex] = val;
	}
	
	//returns the bits between startBitIndex and endBitIndex (both inclusive)
	//as an integer
	//assumes unsigned integer	
	public int getInteger(int startBitIndex, int endBitIndex) {
		int toBeReturned = 0;
		for(int i = startBitIndex; i <= endBitIndex; i++) {
			toBeReturned = toBeReturned << 1;
			int bit = (value[i]==true?1:0);
			toBeReturned = toBeReturned + bit;
		}
		return toBeReturned;
	}
	
	//sets the bits between startBitIndex and endBitIndex (both inclusive)
	//assumes unsigned integer
	public void setInteger(int startBitIndex, int endBitIndex, int val) {
		String bitStr = Integer.toBinaryString(val);
		int strIndex = bitStr.length() - 1;
		for(int i = endBitIndex; i >= startBitIndex; i--) {
			if(strIndex >= 0) {
				if(bitStr.charAt(strIndex) == '0') {
					value[i] = false;
				} else {
					value[i] = true;
				}
				strIndex--;
			} else {
				value[i] = false;
			}
		}
	}
	
	public int getNumBits() {
		return numBits;
	}	
}