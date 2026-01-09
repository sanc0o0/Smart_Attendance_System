type Props = {
    title: string;
    value: number;
};

export default function AnalyticsCard({ title, value }: Props) {
    return (
        <div className="p-4 bg-white rounded-2xl shadow text-center">
            <h3 className="text-sm text-gray-500">{title}</h3>
            <p className="text-2xl font-bold">{value}</p>
        </div>
    );
}
  