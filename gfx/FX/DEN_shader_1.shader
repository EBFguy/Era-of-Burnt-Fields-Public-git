Includes = {
}

PixelShader =
{
	Samplers =
	{
		TextureOne =
		{
			Index = 0
			MagFilter = "Point"
			MinFilter = "Point"
			MipFilter = "None"
			AddressU = "Wrap"
			AddressV = "Wrap"
		}
		TextureTwo =
		{
			Index = 1
			MagFilter = "Point"
			MinFilter = "Point"
			MipFilter = "None"
			AddressU = "Wrap"
			AddressV = "Wrap"
		}
	}
}


VertexStruct VS_INPUT
{
	float4 vPosition  : POSITION;
	float2 vTexCoord  : TEXCOORD0;
};

VertexStruct VS_OUTPUT
{
	float4  vPosition : PDX_POSITION;
	float2  vTexCoord0 : TEXCOORD0;
};


ConstantBuffer( 0, 0 )
{
	float4x4 WorldViewProjectionMatrix; 
	float4 vFirstColor;
	float4 vSecondColor;
	float CurrentState;
};


VertexShader =
{
	MainCode VertexShader
	[[
		
		VS_OUTPUT main(const VS_INPUT v )
		{
			VS_OUTPUT Out;
		   	Out.vPosition  = mul( WorldViewProjectionMatrix, v.vPosition );
			Out.vTexCoord0  = v.vTexCoord;
			Out.vTexCoord0.y = -Out.vTexCoord0.y;
		
			return Out;
		}
		
	]]
}

PixelShader =
{
	MainCode PixelColor
	[[
		
		float4 main( VS_OUTPUT v ) : PDX_COLOR
		{
			if( v.vTexCoord0.x <= CurrentState )
				return vFirstColor;
			else
				return vSecondColor;
		}
		
	]]

	MainCode PixelTexture
	[[
		
		float4 main( VS_OUTPUT v ) : PDX_COLOR
		{
			float inVal = CurrentState * 2000.f;
			float4 origTex = tex2D(TextureOne, v.vTexCoord0);

			if (origTex.a == 0) {
				return float4(0, 0, 0, 0);
			}

			float opacity = floor(inVal / 10.f);
			float colour = inVal - (opacity * 10.f);

			float adjustedOpacity = 1;
			
			float4 outColour = origTex;
			
			if (colour == 1 && origTex.a == 1) {
				outColour.r = 1;
				outColour.g = 1;
				outColour.b = 1;
			}
			if (colour == 1 && origTex.a < 1) {
				outColour.r = outColour.r * 0.3 + 1 * 0.7;
				outColour.g = outColour.g * 0.3 + 1 * 0.7;
				outColour.b = outColour.b * 0.3 + 1 * 0.7;
			}
			if (colour == 2 && origTex.a == 1) {
				outColour.r = 0.50;
				outColour.g = 0;
				outColour.b = 0;
			}
			if (colour == 2 && origTex.a < 1) {
				outColour.r = outColour.r * 0.3 + 0.50 * 0.7;
				outColour.g = outColour.g * 0.3 + 0 * 0.7;
				outColour.b = outColour.b * 0.3 + 0 * 0.7;
			}
			if (colour == 3 && origTex.a == 1) {
				outColour.r = 0.46;
				outColour.g = 0.72;
				outColour.b = 0.92;
			}
			if (colour == 3 && origTex.a < 1) {
				outColour.r = outColour.r * 0.3 + 0.46 * 0.7;
				outColour.g = outColour.g * 0.3 + 0.72 * 0.7;
				outColour.b = outColour.b * 0.3 + 0.92 * 0.7;
			}

			float mapW = vFirstColor.r * 1000.f;
			float mapH = vFirstColor.g * 1000.f;

			float size = 120;
			if (mapW < 100) {
				size = 80;
			}
			if (mapW < 75) {
				size = 60;
			}
			if (mapW < 50) {
				size = 40;
			}

			float rescale = size / mapW;
			if (mapW > mapH) {
				rescale = size / mapH;
			} 

			float imgX = (v.vTexCoord0.x - (1.0 - rescale)/2) / rescale;
			float imgY = (v.vTexCoord0.y + (1.0 - rescale)/2) / rescale;

			if (mapW > mapH) {
				float toRemove = (mapW - mapH) / (2 * mapW);
				imgX = (imgX - toRemove) / (1.0 - 2 * toRemove);
			} else {
				float toRemove = (mapH - mapW) / (2 * mapH);
				imgY = (imgY + toRemove) / (1.0 - 2 * toRemove);
			}

			bool onEdge = tex2D(TextureOne, v.vTexCoord0.xy + float2(2/mapW, 2/mapH)).a == 0
						|| tex2D(TextureOne, v.vTexCoord0.xy + float2(-2/mapW, -2/mapH)).a == 0
						|| tex2D(TextureOne, v.vTexCoord0.xy + float2(2/mapW, -2/mapH)).a == 0
						|| tex2D(TextureOne, v.vTexCoord0.xy + float2(-2/mapW, 2/mapH)).a == 0
						|| tex2D(TextureOne, v.vTexCoord0.xy + float2(2/mapW, 0/mapH)).a == 0
						|| tex2D(TextureOne, v.vTexCoord0.xy + float2(-2/mapW, 0/mapH)).a == 0
						|| tex2D(TextureOne, v.vTexCoord0.xy + float2(0/mapW, -2/mapH)).a == 0
						|| tex2D(TextureOne, v.vTexCoord0.xy + float2(0/mapW, 2/mapH)).a == 0;

			float4 overlayColour = float4(0, 0, 0, 0);

			if (imgX > 0.001f && imgX < 1 && imgY <= 0  && imgY >= -1 && !onEdge) {
				overlayColour = tex2D(TextureTwo, float2((colour - 1 + imgX) * (1.0f / 4), imgY));
			}

			if (overlayColour.a == 1) {
				outColour.rgb = overlayColour.rgb;
			}

			if (origTex.a < 1) {
				adjustedOpacity = lerp(0, 0.4, opacity / 100) * origTex.a / origTex.a;
			}

			if (overlayColour.a == 1) {
				outColour.rgb = overlayColour.rgb;
				adjustedOpacity = lerp(0, 1, opacity / 100) * origTex.a / origTex.a;
			}

			if (opacity == 100) {
				adjustedOpacity = 0.5;
			}

			return float4(outColour.r, outColour.g, outColour.b, adjustedOpacity);
		}
		
	]]
}


BlendState BlendState
{
	BlendEnable = yes
	SourceBlend = "SRC_ALPHA"
	DestBlend = "INV_SRC_ALPHA"
}


Effect Color
{
	VertexShader = "VertexShader"
	PixelShader = "PixelColor"
}

Effect Texture
{
	VertexShader = "VertexShader"
	PixelShader = "PixelTexture"
}

