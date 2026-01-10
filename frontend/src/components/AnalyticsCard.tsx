type Props = {
    title: string;
    value: number;
    accent?: "blue"| "green"
};

const accentMap = {
    blue: "border-blue-500 text-blue-600 bg-blue-50",
    green: "border-green-500 text-green-600 bg-green-50",
}
export default function AnalyticsCard({ title, value, accent = "blue" }: Props) {
    return (
        <div
            className={`bg-blue-50 rounded-xl border-2 ${accentMap[accent]
                } shadow-sm px-6 py-5 flex flex-col justify-center`}
        >
            <span className="text-sm text-gray-500 font-medium">
                {title}
            </span>

            <span className="mt-2 text-3xl font-bold">
                {value}
            </span>
        </div>
    );
}
  