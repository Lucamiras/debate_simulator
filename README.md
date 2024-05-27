# Debate Simulator
The idea behind this project is to host a virtual debate. This could be used to prepare for an actual debate, to quickly gauge two sides of an argument, or to simply have some fun. The debates are created via prompting an LLM of your choice in a specific way. This project was created with a local copy of Llama 3 using Ollama, but by using Langchain, any available model could work.

![Debate Simulator Image](/images/debate_simulator.png)
*An example debate is conducted.* 

# Run it yourself
1. Clone this repository
```bash
git clone git@github.com:Lucamiras/debate_simulator.git
```
2. Create a new environment (for example with Anaconda), then activate it.
```bash
conda create -n [YOUR ENV NAME]
conda activate [YOUR ENV NAME]
```
3. Install the requirements
```bash
pip install -r requirements.txt
```
4. Download Llama 3
```bash
ollama pull llama3
```
5. Run the debate simulator with Streamlit
```bash
streamlit run main.py
```

# Features
- **Debate anything**: Use the free text field to query the two virtual guests to debate. Ideally, this is a two-sided issue so either virtual guest can take part.
- **Debate styles**: Choose from a list of styles, such as `heated` or `casual`.
- **Rounds**: Each debate begins with opening statements, after which the debate continues for n rounds.
- **Host summary**: After n rounds have been completed, a virtual host summarizes the debate and chooses a winner.
- **Debate summary sidebar**: On the left-hand side, each debate is summarized for easy skimming.

# Work in progress ...
This project is being developed on an ongoing basis. Features to include in the future:
- Text-to-speech
- Q&A with debaters
- Panel of judges
- Custom personalities and names for debaters