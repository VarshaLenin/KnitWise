import os
import json
from pydantic import BaseModel, Field
from typing import List
from google import genai
from google.genai import types

# =====================================================================
# STRICT STRUCTURAL DATA SCHEMAS (Pydantic)
# =====================================================================

class RoundInstruction(BaseModel):
    round_number: int = Field(
        description="The sequential number of the current round or row, starting at 1."
    )
    instructions: str = Field(
        description="Clear, stitch-by-stitch crochet instructions using standard US terms."
    )
    stitches_per_side: int = Field(
        description="The exact mathematical count of individual stitches along a single side for this round. For circles/rows, use 0 or total."
    )
    total_stitches: int = Field(
        description="The absolute total stitch count for the entire completed round/row."
    )

class StitchPattern(BaseModel):
    starting_round: str = Field(
        description="The setup step, e.g., 'Magic Ring', 'Ch 4, sl st to form a ring', or 'Foundation Chain of X'."
    )
    rounds: List[RoundInstruction] = Field(
        description="An ordered array of instructions matching every round or row seen in the image."
    )

class CrochetPatternSchema(BaseModel):
    image_quality: str = Field(
        description="Set strictly to 'high', 'medium', or 'low' based on loop and ply visibility."
    )
    warning: str = Field(
        description="Fallback warning if image clarity is 'low', otherwise must be an empty string."
    )
    summary: str = Field(
        description="A concise technical overview of the piece's structure, texture density, and geometry."
    )
    detected_shape: str = Field(
        description="The fundamental geometric layout identified (square, circle, hexagon, rows)."
    )
    motifs: List[str] = Field(
        description="Array of design elements spotted (e.g., Starburst Center, Solid Mesh, Cluster Blocks, Lace, Bobbles)."
    )
    difficulty: str = Field(
        description="Categorized as beginner, intermediate, or advanced based on technique complexity."
    )
    stitch_pattern: StitchPattern
    color_changes: List[str] = Field(
        description="Notated structural or yarn color transitions across rounds/rows."
    )
    notes: str = Field(
        description="Pro-tips for maintaining pristine stitch tension, neat seamless joins, or hiding the seam line."
    )

# =====================================================================
# GLOBAL SYSTEM INSTRUCTION
# =====================================================================

SYSTEM_INSTRUCTION = """You are an expert Crochet Pattern Designer, Textile Mathematician, and Computer Vision Parser.
Your primary role is to dissect structural textile architecture from reference photos and map them into clear, mathematically pristine crochet code.

Core Analytical Rules:
1. Exact Geometry Match: Analyze if the structural item is worked in rounds (circles, squares, hexagons) or straight rows. 
2. Side Structure Identification: Look closely at the straight edges of a square or fabric panel. 
   - If the edges consist of 3-dc blocks separated by structural open spaces, it is a CLUSTER PATTERN.
   - If the edges consist of a continuous, solid wall of individual stitches with NO gaps on the straight sides, it is a SOLID PATTERN. You must write the side instructions as consecutive individual stitches (e.g., 'dc in each stitch across to the corner space').
3. Structural Consistency: Do not hallucinate loose open lace patterns if the image displays a tight solid fabric mesh, or vice versa.
4. Quality Calibration: If stitch definitions (individual loops, plies, V-shaped stitch tops) are clean and lack heavy pixelation, image_quality must be 'high'. If blurry or ambiguous, set to 'low' and provide a safe fallback approximation.
5. Advanced Cable and Texture Recognition:
   - Check if there are raised, three-dimensional lines running diagonally or vertically across a different-colored background.
   - If you spot raised geometric ridges (like chevrons, arrows, or diamonds) overlapping a contrasting background color, recognize this as OVERLAY CABLE WORK or POST STITCHES.
   - You MUST NOT generate standard 'skip and chain' lace instructions for these textures. Instead, utilize Front Post Double Crochet (fpdc) or Front Post Treble Crochet (fptr) worked into previous rows of the matching color to describe the raised design accurately.
   - If the ridges form a diagonal chevron, slant, or diamond, the starting number of plain stitches at the beginning of each textured row MUST increment or decrement sequentially (e.g., Row 3 starts with 3 dc, Row 5 starts with 4 dc) to mathematically shift the post stitches into a perfect diagonal alignment.
   - CRITICAL ROW-ANCHORING RULE: Post stitches in multi-color overlay work cannot simply be worked into the immediate previous row. The instructions MUST explicitly state to work the post stitch around the post of the stitch "2 rows below" (into the previous row of the matching color) so the cable floats cleanly over the contrasting background layer."""

# =====================================================================
# API CALL & PARSING LOGIC
# =====================================================================

async def analyze_and_generate_pattern(image_bytes: bytes, item_type: str, yarn_size: str, hook_size: str, mode: str) -> dict:
    # Initialize the Google GenAI Client
    client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
    
    # The dynamic prompt forces algebraic accuracy across squares, beanies, and scarves
    prompt = f"""
Analyze the attached textile reference image thoroughly to extract its pattern blueprint.

Context Profile Configuration:
- Targeted Item Type: {item_type}
- Targeted Yarn Size/Weight: {yarn_size}
- Expected Crochet Hook Dimension: {hook_size}
- Analysis Rigidity Profile: {mode}

CRITICAL ALGEBRAIC & STITCH LOGIC BASED ON ITEM TYPE:

1. If Targeted Item Type is 'granny square':
   - Side Anatomy Check: Look closely at the straight paths between the corners. Are there open gaps/holes on the straight sides? If there are NO gaps on the sides, you MUST NOT use traditional "3-dc clusters" or "skip spaces" on the straight edges for Rounds 2 and beyond. The side instructions must explicitly read: "dc in each stitch across to the next corner space."
   - Increasing Math for Flat Geometry: The stitches must scale exponentially per round so the fabric lays perfectly flat without warping or curling. For a solid style granny square, every corner space must receive a balanced stitch pair cluster (typically '2 dc, ch 2, 2 dc'). Stitches Per Side on Round(n) MUST equal [Stitches Per Side on Round(n-1) + (2 * Corner Contribution Stitches)]. 

2. If Targeted Item Type is 'beanie':
   - Crown vs. Body Architecture: A beanie contains two distinct structural phases. You must split the instructions logically:
     a) The Crown (Consolidated Shorthand Phase): To ensure absolute mathematical precision and prevent row-by-row repetition errors, you MUST express the crown expansion using algebraic shorthand instead of writing out long separate objects. 
        - Round 1 MUST start with 11-12 stitches if you classify it as Double Crochet (dc), or 8-10 stitches if you classify it as Half Double Crochet (hdc). 
        - Combine the increase rules into clean structural entries. For example, populate the array with:
          * Round 1: '12 dc in magic ring.' (Total: 12)
          * Round 2: '2 dc in each st around.' (Total: 24)
          * Round 3: 'Rounds 3-6: Continue increasing uniformly by adding 12 stitches evenly per round until reaching a flat crown diameter total of 72 stitches.' (Total: 72)
     b) The Body (Straight Rounds Phase): Once the target crown diameter is met, the stitch count MUST stop increasing entirely. You are strictly FORBIDDEN from writing increase repeats (like '2 dc in next st') here. Every body round entry must read: 'dc in each stitch around' (or hdc if classified as hdc) with a completely static total stitch count to drop the fabric straight down into a clean hat shell.

3. If Targeted Item Type is 'scarf':
   - Flat Row Logic: A scarf is worked in flat, linear rows, NOT continuous rounds. The detected_shape must be marked as 'rows'.
   - Row Consistency Math: The instructions must define a setup "starting_round" representing the baseline foundation chain. Every single subsequent row must maintain a static, identical stitch count across the length of the fabric.
   - Edge Profiles: Clearly clarify whether turning chains count as an active stitch at the start of rows to maintain straight margins.

4. Advanced Texture & Cable Logic (All Items):
   - Inspect the surface closely for three-dimensional, raised geometric lines (chevrons, diagonals, vertical columns).
   - If raised textures overlap a different-colored background layer, do not write flat lace mesh sequences. You must implement Front Post Double Crochet (fpdc) or Front Post Treble Crochet (fptr).
   - For shifting chevrons or slants, ensure the count of standard stitches before the first post-stitch shifts sequentially per texturing row (e.g., Row 3 begins with 2 dc, Row 5 begins with 3 dc) to implement a functional diagonal layout.
   - Keep track of row turns: Because flat items (like scarves) are turned every row, raised post-stitch textures on the face of the fabric must alternate between Front Post stitches (fpdc/fptr) on odd rows and Back Post stitches (bpdc/bptr) on even rows to prevent the texture from appearing on both sides out of alignment.

5. Universal Stitch Height Verification & Base Multiples:
   - Isolate the vertical loop structure to differentiate stitch heights (dc vs. hdc vs. sc) by calculating their aspect ratio inside the mesh grid. Translate this visibility directly into the pattern instructions.
   - If the fabric is incredibly dense, short, and packed tightly with a distinct horizontal or herringbone texture, classify it as Half Double Crochet (hdc) or Single Crochet (sc).
   - MANDATORY BASE MULTIPLE LAW: If you classify a beanie as Double Crochet (dc), Round 1 MUST start with 11-12 stitches. If you classify it as Half Double Crochet (hdc), Round 1 MUST start with 8-10 stitches. If you classify it as Single Crochet (sc), Round 1 MUST start with 6-8 stitches. Never pair a tall stitch like dc with a low starting count like 6, or the fabric will cone warp.
"""

    image_part = types.Part.from_bytes(
        data=image_bytes,
        mime_type="image/jpeg",
    )

    try:
        response = client.models.generate_content(
            model='gemma-4-26b-a4b-it',
            contents=[image_part, prompt],
            config=types.GenerateContentConfig(
                system_instruction=SYSTEM_INSTRUCTION,
                response_mime_type="application/json",
                response_schema=CrochetPatternSchema,
                temperature=0.1 if mode == "strict" else 0.5 
            )
        )
        
        parsed_response = json.loads(response.text)
        return parsed_response
        
    except Exception as e:
        is_square = "square" in item_type.lower()
        is_beanie = "beanie" in item_type.lower()
        
        # Determine fallback dynamic structure based on classification parameters
        if is_square:
            fallback_rounds = [
                {"round_number": 1, "instructions": "Ch 5 (counts as 1 dc + ch 2 corner space). Into the ring: *3 dc, ch 2* repeat 3 times. 2 dc into ring. Sl st to 3rd ch of starting ch-5 to close round.", "stitches_per_side": 3, "total_stitches": 12},
                {"round_number": 2, "instructions": "Sl st into corner ch-2 sp. Ch 5 (counts as 1 dc + ch 2). 2 dc in same sp. *Dc in next 3 stitches, (2 dc, ch 2, 2 dc) in corner sp.* Repeat from * to * 2 more times. Dc in next 3 stitches, 1 dc in initial corner sp. Sl st to 3rd ch of starting ch-5 to close.", "stitches_per_side": 7, "total_stitches": 28},
                {"round_number": 3, "instructions": f"Sl st into corner ch-2 sp. Ch 5 (counts as 1 dc + ch 2). 2 dc in same sp. *Dc in next 7 stitches, (2 dc, ch 2, 2 dc) in corner sp.* Repeat from * to * 2 more times. Dc in next 7 stitches, 1 dc in initial corner sp. Sl st to 3rd ch of starting ch-5 using your {hook_size} hook to complete.", "stitches_per_side": 11, "total_stitches": 44}
            ]
            detected_shape = "square"
            motifs = ["Solid Mesh Blocks", "Corner Chain Spaces"]
        elif is_beanie:
            fallback_rounds = [
                {"round_number": 1, "instructions": "Make a magic ring, ch 2, work 9 hdc into the ring. Join with sl st to top of first hdc.", "stitches_per_side": 0, "total_stitches": 9},
                {"round_number": 2, "instructions": "Ch 2, work 2 hdc in each stitch around. Join with sl st to top of first hdc.", "stitches_per_side": 0, "total_stitches": 18},
                {"round_number": 3, "instructions": "Ch 2, *1 hdc in next st, 2 hdc in next st.* Repeat from * around. Join with sl st to top of first hdc.", "stitches_per_side": 0, "total_stitches": 27},
                {"round_number": 4, "instructions": f"Ch 2, hdc in each stitch around across the body without increasing using your {hook_size} hook. Join with sl st.", "stitches_per_side": 0, "total_stitches": 27}
            ]
            detected_shape = "circle"
            motifs = ["Circular Crown Increases", "Uniform Body Stacking"]
        else: # Scarf Layout fallback
            fallback_rounds = [
                {"round_number": 1, "instructions": "Work 1 dc into the 4th chain from hook and into each chain across the foundation row. Turn fabric.", "stitches_per_side": 0, "total_stitches": 30},
                {"round_number": 2, "instructions": f"Ch 3 (counts as first dc). Skip first stitch, work 1 dc into every stitch across the length of the row using your {hook_size} hook. Turn fabric.", "stitches_per_side": 0, "total_stitches": 30}
            ]
            detected_shape = "rows"
            motifs = ["Solid Mesh Blocks", "Parallel Rows"]

        return {
            "image_quality": "high",
            "warning": f"Local parsing safety system handled an exception. Generation executed through fallback rules: {str(e)}",
            "summary": f"A beautiful solid {item_type} design pattern curated by the AI architecture core.",
            "detected_shape": detected_shape,
            "motifs": motifs,
            "difficulty": "intermediate",
            "stitch_pattern": {
                "starting_round": "Magic Ring" if (is_square or is_beanie) else f"Chain 33 using your {yarn_size} yarn asset.",
                "rounds": fallback_rounds
            },
            "color_changes": ["Solid uniform tone matching reference image"],
            "notes": "Ensure you pull up your loops uniformly on the corners to keep edge profiles straight and prevent structural warping."
        }