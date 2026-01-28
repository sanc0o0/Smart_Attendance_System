type Props = {
    data: {
        name: string;
        present_days: number;
        total_days: number;
    }[];
};

export default function StudentTable({ data }: Props) {
    if (data.length === 0) {
        return (
            <p className="text-gray-400 text-center">
                No attendance data yet.
            </p>
        );
    }

    return (
        <div className="bg-white rounded-xl shadow-sm mt-8 overflow-hidden">
            {/* Header */}
            <div className="px-6 py-4 border-b border-gray-400">
                <h2 className="text-lg font-bold">
                    Attendance Leaderboard
                </h2>
            </div>

            <table className="w-full text-sm">
                <thead className="border-b border-gray-400 bg-gray-50 text-black">
                    <tr>
                        <th className="px-6 py-3 text-left">Rank</th>
                        <th className="px-6 py-3 text-left">Student</th>
                        <th className="px-6 py-3 text-right">Days Present</th>
                        <th className="px-6 py-3 text-right">Percentage</th>
                    </tr>
                </thead>

                <tbody>
                    {data.map((student, index) => {
                        const percentage = student.total_days === 0? 0
                        :Math.round(
                            (student.present_days / student.total_days) * 100
                        );

                        return (
                            <tr
                                key={student.name}
                                className="hover:bg-gray-50"
                            >
                                <td className="px-6 py-3 font-medium">
                                    #{index + 1}
                                </td>
                                <td className="px-6 py-3">
                                    {student.name}
                                </td>
                                <td className="px-6 py-3 text-right">
                                    {student.present_days}
                                </td>
                                <td className="px-6 py-3 text-right font-semibold">
                                    {percentage}%
                                </td>
                            </tr>
                        );
                    })}
                </tbody>
            </table>
        </div>
    );
}
