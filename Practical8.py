
MOD = 1000000007
NEG = -10**30

def main():
    try:
        n, m = map(int, input().split())
        matrix = []

        for _ in range(n):
            row = input().split()

            if len(row) != m:
                print("Invalid matrix.")
                return

            matrix.append([
                None if x == "X" else int(x)
                for x in row
            ])

        if matrix[0][0] is None or matrix[n-1][m-1] is None:
            print("IMPOSSIBLE")
            return

        score = [NEG] * m
        ways = [0] * m

        for i in range(n):
            new_score = [NEG] * m
            new_ways = [0] * m

            for j in range(m):
                if matrix[i][j] is None:
                    continue

                if i == 0 and j == 0:
                    new_score[j] = matrix[i][j]
                    new_ways[j] = 1
                    continue

                best = NEG
                count = 0

                for pi, pj in (
                    (i-1, j), (i, j-1), (i-1, j-1)
                ):
                    if pi < 0 or pj < 0:
                        continue

                    if pi == i-1:
                        s, w = score[pj], ways[pj]
                    else:
                        s, w = new_score[pj], new_ways[pj]

                    if s > best:
                        best = s
                        count = w
                    elif s == best:
                        count = (count + w) % MOD

                if best != NEG:
                    new_score[j] = best + matrix[i][j]
                    new_ways[j] = count

            score, ways = new_score, new_ways

        if score[m-1] == NEG:
            print("IMPOSSIBLE")
        else:
            print(score[m-1], ways[m-1] % MOD)

    except (ValueError, IndexError):
        print("Invalid input.")

if __name__ == "__main__":
    main()
