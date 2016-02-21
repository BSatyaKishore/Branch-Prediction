
public abstract class Predictor {

	public Predictor() {}


	abstract public void Train(long address, boolean outcome, boolean predict);

	abstract public boolean predict(long address);
}