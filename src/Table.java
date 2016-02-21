

public class Table {
	private int numEntries;
	private int bitsPerEntry;
	private Register values[];
	
	public Table(int entries,int bits){
		numEntries=entries;
		bitsPerEntry=bits;	
		values=new Register[numEntries];
		for (int i = 0; i < numEntries; i++) {
			values[i]=new Register(bitsPerEntry);
		}
	}
	
	public boolean getBit(int tableIndex,int bitIndex){
		return values[tableIndex].getBitAtIndex(bitIndex);
	}

	public void setBit(int rowIndex,int bitIndex,boolean val){
		values[rowIndex].setBitAtIndex(bitIndex, val);
	}
	
	//returns the bits between startBitIndex and endBitIndex (both inclusive)
	//as an integer
	//assumes unsigned integer	
	public int getInteger(int rowIndex,int startBitIndex, int endBitIndex){
		return values[rowIndex].getInteger(startBitIndex, endBitIndex);
	}

	//sets the bits between startBitIndex and endBitIndex (both inclusive)
	//assumes unsigned integer
	public void setInteger(int rowIndex,int startBitIndex, int endBitIndex, int val){
		values[rowIndex].setInteger(startBitIndex, endBitIndex, val);
	}

	public int getNumEntries() {
		return numEntries;
	}

	public int getBitsPerEntry() {
		return bitsPerEntry;
	}	
}