from fasthtml.common import *
from shad4fast import *
import logging
from starlette.staticfiles import StaticFiles
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Create FastHTML app
app, rt = fast_app(
    pico=False,
    hdrs=(
        ShadHead(tw_cdn=True, theme_handle=False),
        Link(
            rel="stylesheet",
            href="/static/style.css",
            type="text/css"
        ),
        Script(
            src="/static/script.js",
            type="text/javascript",
            defer=True
        ),
    )
)

# Mount static files (CSS, JS)
app.mount("/static", StaticFiles(directory="static"), name="static")

# Define the main layout of the frontend
def get_main_layout():
    return Div(
        # Header
        Header(
            Div(
                H1("AI-Powered Multi-Agent Coding Assistant", cls="text-2xl font-bold text-white"),
                cls="container mx-auto px-4 py-6"
            ),
            cls="bg-zinc-900 shadow-md"
        ),

        # Main content
        Main(
            Div(
                # Tabs for different functionalities
                Tabs(
                    TabsList(
                        TabsTrigger(
                            Div(Lucide("code", cls="w-4 h-4 mr-2"), "Code Generator", cls="flex items-center"),
                            value="code-generator",
                            cls="data-[state=active]:bg-zinc-800 data-[state=active]:text-white text-gray-400 hover:text-white"
                        ),
                        TabsTrigger(
                            Div(Lucide("bug", cls="w-4 h-4 mr-2"), "Debugger", cls="flex items-center"),
                            value="debugger",
                            cls="data-[state=active]:bg-zinc-800 data-[state=active]:text-white text-gray-400 hover:text-white"
                        ),
                        TabsTrigger(
                            Div(Lucide("zap", cls="w-4 h-4 mr-2"), "Optimizer", cls="flex items-center"),
                            value="optimizer",
                            cls="data-[state=active]:bg-zinc-800 data-[state=active]:text-white text-gray-400 hover:text-white"
                        ),
                        cls="grid w-full grid-cols-3 bg-zinc-900 rounded-lg gap-1 border border-zinc-800"
                    ),
                    TabsContent(
                        Div(
                            # Code Generator Section
                            Div(
                                Textarea(
                                    placeholder="Enter your coding prompt here...",
                                    id="code-prompt",
                                    cls="w-full p-4 bg-zinc-800 text-white rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                                ),
                                Button(
                                    "Generate Code",
                                    id="generate-code-btn",
                                    cls="mt-4 px-6 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700"
                                ),
                                cls="space-y-4"
                            ),
                            Div(
                                # Generated code display
                                Div(
                                    H2("Generated Code", cls="text-xl font-bold text-white"),
                                    Pre(
                                        Code(id="generated-code", cls="text-sm text-white"),
                                        cls="p-4 bg-zinc-800 rounded-lg mt-4"
                                    ),
                                    cls="mt-6"
                                ),
                                cls="space-y-6"
                            ),
                            cls="space-y-6"
                        ),
                        value="code-generator",
                        cls="space-y-7 transition-all duration-500 ease-in-out"
                    ),
                    TabsContent(
                        Div(
                            # Debugger Section
                            Div(
                                Textarea(
                                    placeholder="Paste your code here to debug...",
                                    id="debug-code-input",
                                    cls="w-full p-4 bg-zinc-800 text-white rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                                ),
                                Button(
                                    "Debug Code",
                                    id="debug-code-btn",
                                    cls="mt-4 px-6 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700"
                                ),
                                cls="space-y-4"
                            ),
                            Div(
                                # Debugged code display
                                Div(
                                    H2("Debugged Code", cls="text-xl font-bold text-white"),
                                    Pre(
                                        Code(id="debugged-code", cls="text-sm text-white"),
                                        cls="p-4 bg-zinc-800 rounded-lg mt-4"
                                    ),
                                    cls="mt-6"
                                ),
                                cls="space-y-6"
                            ),
                            cls="space-y-6"
                        ),
                        value="debugger",
                        cls="space-y-7 transition-all duration-500 ease-in-out"
                    ),
                    TabsContent(
                        Div(
                            # Optimizer Section
                            Div(
                                Textarea(
                                    placeholder="Paste your code here to optimize...",
                                    id="optimize-code-input",
                                    cls="w-full p-4 bg-zinc-800 text-white rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                                ),
                                Button(
                                    "Optimize Code",
                                    id="optimize-code-btn",
                                    cls="mt-4 px-6 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700"
                                ),
                                cls="space-y-4"
                            ),
                            Div(
                                # Optimized code display
                                Div(
                                    H2("Optimized Code", cls="text-xl font-bold text-white"),
                                    Pre(
                                        Code(id="optimized-code", cls="text-sm text-white"),
                                        cls="p-4 bg-zinc-800 rounded-lg mt-4"
                                    ),
                                    cls="mt-6"
                                ),
                                cls="space-y-6"
                            ),
                            cls="space-y-6"
                        ),
                        value="optimizer",
                        cls="space-y-7 transition-all duration-500 ease-in-out"
                    ),
                    default_value="code-generator",
                    cls="w-full max-w-7xl mx-auto space-y-7"
                ),
                cls="container mx-auto px-4 py-8"
            ),
            cls="flex-1"
        ),

        # Footer
        Footer(
            Div(
                P("© 2023 AI-Powered Multi-Agent Coding Assistant", cls="text-center text-gray-400"),
                cls="container mx-auto px-4 py-6"
            ),
            cls="bg-zinc-900 shadow-md"
        ),
        cls="min-h-screen flex flex-col bg-zinc-950 text-white"
    )

# Define the root route
@app.route("/")
async def root():
    return get_main_layout()

# Run the app
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)