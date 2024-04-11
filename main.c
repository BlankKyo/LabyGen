#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>
#include <assert.h>

int mazeid[2005][2005], idcells[1000005][2];
char maze[2005][2005];
void swap(int* a, int* b) {
int t = *a;
*a = *b;
*b = t;
}
// a structure to represent an edge in graph
struct Edge {
    int src, dest;
};

// a structure to represent a graph
struct Graph {
    // V-> Number of vertices, E-> Number of edges
    int V, E;

    // graph is represented as an array of edges
    struct Edge* edge;
};
struct Graph* createGraph(int V, int E)
{
    struct Graph* graph = (struct Graph*)malloc(sizeof(struct Graph));
    graph->V = V;
    graph->E = E;

    graph->edge = (struct Edge*)malloc(graph->E * sizeof(struct Edge));

    return graph;
}
void DestroyGraph(struct Graph* graph){
    free(graph->edge);
    free(graph);
}

//DSU functions O(log(n))
int link[1000005], size[1000005];

int find(int x) {
    while (x != link[x]) x = link[x];
    return x;
}

void unite(int a, int b) {
    a = find(a);
    b = find(b);
    if (size[a] < size[b]) swap(&a, &b);
    size[a] += size[b];
    link[b] = a;
}

void shuffle(struct Edge* array, size_t n){ //function that shuffles an array
    if (n > 1){
        size_t i;
        for (i = 0; i < n - 1; i++){
            size_t j = i + rand() / (RAND_MAX / (n - i) + 1); //rand() generates a random int in [0, RAND_MAX) ==> rescaling
            struct Edge t = array[j];
            array[j] = array[i];
            array[i] = t;
        }
    }
}










int main(int argc, char** argv) {
    int n, m; // 2 * n + 1 rows and 2 * m + 1 columns
    char *ns, *ms;
    ns = argv[1], ms = argv[2];
    n = atoi(ns);
    m = atoi(ms);
    for (int i = 1; i <= 1000000; i++) link[i] = i;
    for (int i = 1; i <= 1000000; i++) size[i] = 1;
    struct Graph* graph = createGraph(n * m, 2 * n * m - (n + m)); //for each row calculate down + right node
    n *= 2, m *= 2; //between each 2 cells we insert a wall indicator
    int i, j, current = 0;
    memset(maze, 'W', sizeof(maze)); //initialize maze full of walls
    memset(mazeid, 0, sizeof(mazeid)); //cell -> id
    memset(idcells, 0, sizeof(idcells)); //id -> cell
    //possible edges in the graph
    for (i = 1; 2 * i - 1 <= n; i++){
        for (j = 1; 2 * j - 1 <= m; j++){
            mazeid[2 * i - 1][2 * j - 1] = (i - 1) * (m / 2) + j - 1; //index nodes
            idcells[(i - 1) * (m / 2) + j - 1][0] = 2 * i - 1;
            idcells[(i - 1) * (m / 2) + j - 1][1] = 2 * j - 1;
            if (i * (m / 2) + j - 1 < (n / 2) * (m / 2)) { //node under the current node
                graph->edge[current].src = (i - 1) * (m / 2) + j - 1;
                graph->edge[current++].dest = i * (m / 2) + j - 1;
            }
            if ((i - 1) * (m / 2) + j < i * (m / 2)) { //node to the right of the current node
                graph->edge[current].src = (i - 1) * (m / 2) + j - 1;
                graph->edge[current++].dest = (i - 1) * (m / 2) + j;
            }
        }
    }
    srand(time(NULL)); //seeds the rand() function using time in seconds => better pseudo-random engine
    shuffle(graph->edge, graph->E); //shuffles the edges array
    int* parent = (int*) malloc(graph->V * sizeof(struct Graph)); //create parents array
    memset(parent, -1, sizeof(int) * graph->V); //initialize parents array

    for (i = 0; i < graph->E; i++) {
        int x = find(graph->edge[i].src);
        int y = find(graph->edge[i].dest);

        if (x == y) //Detect Cycle in graph
            continue;
        unite(x, y);
        x = graph->edge[i].src;
        y = graph->edge[i].dest;
        int xi = idcells[x][0], xj = idcells[x][1], yi = idcells[y][0], yj = idcells[y][1];
        maze[xi][xj] = maze[yi][yj] = 'P';
        if (mazeid[xi][xj + 2] == y) maze[xi][xj + 1] = 'P';
        else maze[xi + 1][xj] = 'P';
    }



    FILE *out_file = fopen("laby.txt", "w"); // write only
    assert(out_file != NULL);
    //show mazeid
    /*for (i = 0; i <= n; i++){
        for (j = 0; j <= m; j++){
            printf("%d ", mazeid[i][j]);
        }
        printf("\n");
    }*/
    //show idcells
    /*for (i = 0; i < graph->E; i++) printf("%d %d\n", idcells[i][0], idcells[i][1]);
    printf("\n");*/
    //show possible edges
    /*n /= 2, m /= 2;
    printf("nb of edges: %d \n", graph->E);
    for (i = 0; i < graph->E; i++) {
        printf("%d %d", graph->edge[i].src, graph->edge[i].dest);
        printf("\n");
    }*/
    //show maze
    for (i = 0; i <= n; i++){
        for (j = 0; j <= m; j++){
            //printf("%c ", maze[i][j]);
            fprintf(out_file, "%c ", maze[i][j]); // write to file
        }
        fprintf(out_file, "\n");
    }
    fclose(out_file);
    DestroyGraph(graph);
}
