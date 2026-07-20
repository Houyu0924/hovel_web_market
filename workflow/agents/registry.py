from .market import MarketAgent
from .seo import SeoAgent
from .investment import InvestmentAgent
from .product import ProductAgent
from .writer import WriterAgent
from .factcheck import FactCheckAgent
from .editor import EditorAgent
AGENTS={"market":MarketAgent,"seo":SeoAgent,"investment":InvestmentAgent,"product":ProductAgent,"writer":WriterAgent,"factcheck":FactCheckAgent,"editor":EditorAgent}
def get_agent(name):
    if name not in AGENTS: raise KeyError(f"Unknown agent: {name}")
    return AGENTS[name]()
