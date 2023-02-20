#include <cmath>
#include <iostream>
#include <vector>

using namespace std;

struct vec3d
{
    float x, y, z;
};

struct triangle
{
	vec3d p[3];
};


struct mesh
{
	vector<triangle> tris;
};

struct mat4x4
{
    float m[4][4] = { 0 };
};

void MultiplyMatrixVector(vec3d &i, vec3d &o, mat4x4 &m)
{
    o.x = i.x * m.m[0][0] + i.y * m.m[1][0] + i.z * m.m[2][0] + m.m[3][0];
    o.y = i.x * m.m[0][1] + i.y * m.m[1][1] + i.z * m.m[2][1] + m.m[3][1];
    o.z = i.x * m.m[0][2] + i.y * m.m[1][2] + i.z * m.m[2][2] + m.m[3][2];
    float w = i.x * m.m[0][3] + i.y * m.m[1][3] + i.z * m.m[2][3] + m.m[3][3];

    
   

    if (w != 0.0f)
    {
        o.x /= w; o.y /= w; o.z /= w;
    }
}

int main()
{
    float width = 500;
    float height = 500;
    mat4x4 matProj;
    mesh meshCube;
    float fNear = 0.1f;
    float fFar = 1000.0f;
    float fFov = 90.0f;
    float fAspectRatio = height / width;
    float fFovRad = 1.0f / tanf(fFov * 0.5f / 180.0f * 3.14159f);
    matProj.m[0][0] = fAspectRatio * fFovRad;
    matProj.m[1][1] = fFovRad;
    matProj.m[2][2] = fFar / (fFar - fNear);
    matProj.m[3][2] = (-fFar * fNear) / (fFar - fNear);
    matProj.m[2][3] = 1.0f;
    matProj.m[3][3] = 0.0f;

    meshCube.tris = {

		// SOUTH
		{ 0.0f, 0.0f, 0.0f,    0.0f, 1.0f, 0.0f,    1.0f, 1.0f, 0.0f },
		{ 0.0f, 0.0f, 0.0f,    1.0f, 1.0f, 0.0f,    1.0f, 0.0f, 0.0f },

		// EAST                                                      
		{ 1.0f, 0.0f, 0.0f,    1.0f, 1.0f, 0.0f,    1.0f, 1.0f, 1.0f },
		{ 1.0f, 0.0f, 0.0f,    1.0f, 1.0f, 1.0f,    1.0f, 0.0f, 1.0f },

		// NORTH                                                     
		{ 1.0f, 0.0f, 1.0f,    1.0f, 1.0f, 1.0f,    0.0f, 1.0f, 1.0f },
		{ 1.0f, 0.0f, 1.0f,    0.0f, 1.0f, 1.0f,    0.0f, 0.0f, 1.0f },

		// WEST                                                      
		{ 0.0f, 0.0f, 1.0f,    0.0f, 1.0f, 1.0f,    0.0f, 1.0f, 0.0f },
		{ 0.0f, 0.0f, 1.0f,    0.0f, 1.0f, 0.0f,    0.0f, 0.0f, 0.0f },

		// TOP                                                       
		{ 0.0f, 1.0f, 0.0f,    0.0f, 1.0f, 1.0f,    1.0f, 1.0f, 1.0f },
		{ 0.0f, 1.0f, 0.0f,    1.0f, 1.0f, 1.0f,    1.0f, 1.0f, 0.0f },

		// BOTTOM                                                    
		{ 1.0f, 0.0f, 1.0f,    0.0f, 0.0f, 1.0f,    0.0f, 0.0f, 0.0f },
		{ 1.0f, 0.0f, 1.0f,    0.0f, 0.0f, 0.0f,    1.0f, 0.0f, 0.0f },

		};

        mat4x4 matRotZ, matRotX;
		float fTheta;
        fTheta += 1.0f * 0;

		// Rotation Z
		matRotZ.m[0][0] = cosf(fTheta);
		matRotZ.m[0][1] = sinf(fTheta);
		matRotZ.m[1][0] = -sinf(fTheta);
		matRotZ.m[1][1] = cosf(fTheta);
		matRotZ.m[2][2] = 1;
		matRotZ.m[3][3] = 1;

		// Rotation X
		matRotX.m[0][0] = 1;
		matRotX.m[1][1] = cosf(fTheta * 0.5f);
		matRotX.m[1][2] = sinf(fTheta * 0.5f);
		matRotX.m[2][1] = -sinf(fTheta * 0.5f);
		matRotX.m[2][2] = cosf(fTheta * 0.5f);
		matRotX.m[3][3] = 1;

        for (auto m : matRotZ.m)
        {
            for(int i = 0; i < 4; i++)
            {
                cout << m[i] << " ";
            }
            cout<< endl;
        }
        count << endl;

           for (auto m : matRotX.m)
        {
            for(int i = 0; i < 4; i++)
            {
                cout << m[i] << " ";
            }
            cout<< endl;
        }






        int index =0;
    for( auto tri: meshCube.tris)
    {
        triangle triProjected, triTranslated, triRotatedZ, triRotatedZX;

        // Rotate in Z-Axis
        MultiplyMatrixVector(tri.p[0], triRotatedZ.p[0], matRotZ);
        MultiplyMatrixVector(tri.p[1], triRotatedZ.p[1], matRotZ);
        MultiplyMatrixVector(tri.p[2], triRotatedZ.p[2], matRotZ);

        
        // for (auto vec : triRotatedZ.p)
        // {   
        //     cout<< index << "--> " << vec.x << " " << vec.y << " " << vec.z << endl;
        //     index++;
        // }

        // for (auto vec : tri.p)
        // {   
        //     cout<< index << "--> " << vec.x << " " << vec.y << " " << vec.z << endl;
        //     index++;
        // }



        // Rotate in X-Axis
        MultiplyMatrixVector(triRotatedZ.p[0], triRotatedZX.p[0], matRotX);
        MultiplyMatrixVector(triRotatedZ.p[1], triRotatedZX.p[1], matRotX);
        MultiplyMatrixVector(triRotatedZ.p[2], triRotatedZX.p[2], matRotX);


        // for(auto vec : triRotatedZX.p)
        // {
        //     cout << vec.x << " " << vec.y << " " << vec.z << endl;
        // }




        // Offset into the screen
        triTranslated = triRotatedZX;
        triTranslated.p[0].z = triRotatedZX.p[0].z + 3.0f;
        triTranslated.p[1].z = triRotatedZX.p[1].z + 3.0f;
        triTranslated.p[2].z = triRotatedZX.p[2].z + 3.0f;

        //     for(auto vec : triTranslated.p)
        // {
        //     cout << vec.x << " " << vec.y << " " << vec.z << endl;
        // }
  


        MultiplyMatrixVector(triTranslated.p[0], triProjected.p[0], matProj);
        MultiplyMatrixVector(triTranslated.p[1], triProjected.p[1], matProj);
        MultiplyMatrixVector(triTranslated.p[2], triProjected.p[2], matProj);

        // for(auto vec : triProjected.p)
        // {
        //     cout << vec.x << " " << vec.y << " " << vec.z << endl;
        // }

        // for(auto vec : matProj.m)
        // {
        //     cout << vec[0] << " " << vec[1] << " " << vec[2] << " " << vec[3] << endl;
        // }
        // for(auto vec : triTranslated.p)
        // {
        //     cout << vec.x << " " << vec.y << " " << vec.z << endl;
        // }


        triProjected.p[0].x += 1.0f; triProjected.p[0].y += 1.0f;
        triProjected.p[1].x += 1.0f; triProjected.p[1].y += 1.0f;
        triProjected.p[2].x += 1.0f; triProjected.p[2].y += 1.0f;

        triProjected.p[0].x *= 0.5f * width;
        triProjected.p[0].y *= 0.5f * height;
        triProjected.p[1].x *= 0.5f * width;
        triProjected.p[1].y *= 0.5f * height;
        triProjected.p[2].x *= 0.5f * width;
        triProjected.p[2].y *= 0.5f * height;

        

      
    }

    // vec3d test = {1, 1, 1};
    // vec3d out = {0, 0, 0};
    // MultiplyMatrixVector(test, out, matProj);
    // for(auto vec : matProj.m)
    // {
    //     cout << vec[0] << " " << vec[1] << " " << vec[2] << " " << vec[3] << endl;
    // }
    // cout << out.x << " " << out.y << " " << out.z << endl;

    // cout <<  tanf(fFov * 0.5f / 180.0f * 3.14159f);
    
}

// 0 0 0  0 0 0
// 0 1 0  0 1 0
// 1 1 0  1 1 0
// 0 0 0
// 1 1 0
// 1 0 0
// 1 0 0
// 1 1 0
// 1 1 1
// 1 0 0
// 1 1 1
// 1 0 1
// 1 0 1
// 1 1 1
// 0 1 1
// 1 0 1
// 0 1 1
// 0 0 1
// 0 0 1
// 0 1 1
// 0 1 0
// 0 0 1
// 0 1 0
// 0 0 0
// 0 1 0
// 0 1 1
// 1 1 1
// 0 1 0
// 1 1 1
// 1 1 0
// 1 0 1
// 0 0 1
// 0 0 0
// 1 0 1
// 0 0 0
// 1 0 0

