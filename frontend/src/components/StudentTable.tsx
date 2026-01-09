type Props = {
    data: {
        name: string;
        total_days: number;
    }[];
};

export default function StudentTable({ data }: Props) {
    return (
        <div className="bg-white rounded-2xl shadow p-4">
            <h2 className="font-semibold mb-3">Attendance Leaderboard</h2>
            <table className="w-full text-left ">
                <thead>
                    <tr>
                        <th>Student</th>
                        <th>Total Days</th>
                    </tr>
                </thead>
                <tbody>
                    {data.map((s) => (
                        <tr key={s.name}>
                            <td>{s.name}</td>
                            <td>{s.total_days}</td>
                        </tr>
                    ))}
                </tbody>
            </table>
        </div>
    );
}
  